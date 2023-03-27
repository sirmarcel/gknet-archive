# HIGHLY experimental
import numpy as np
import torch
from torch.autograd import grad

from schnetpack import Properties

from ase import units, Atoms

from gknet.model import Model
from gknet.helpers import guess_device_settings
from gknet import keys

from gknet.experimental.fast_calculator.converter import Converter
from gknet.experimental.fast_calculator.model import Model, disable_property
from gknet.experimental.fast_calculator.comms import comms


class FoldedHeatFluxCalculator:
    def __init__(
        self,
        model,
        device=None,
        virials_reference=None,
        skin=0.1,
        verbose=False,
        report_update=False,
        never_update=False,
    ):

        self.verbose = verbose
        self.reporter = comms.reporter(silent=(not self.verbose))

        self.virials_reference = None

        if virials_reference is not None:
            self.virials_reference = get_reference_atoms(virials_reference)

        if not isinstance(model, Model):
            from torch import load

            if self.verbose:
                comms.talk(f"loading model from {model}")

            tmp = torch.load(model)
            model = Model.from_config(tmp["config"]["model"])
            model.restore(tmp["state"])

        self.model = model
        self.model.training = False  # avoid building graph for second-order derivatives
        self.model.return_pairwise = False  # don't need this
        disable_property(self.model.model, "derivative")  # we don't need forces

        self.device, _ = guess_device_settings(device=device)
        if self.verbose:
            comms.talk(f"UnfoldedHeatFluxCalculator will use device {self.device}.")
        self.model.to(self.device)

        # effective cutoff
        cutoff = model.config_representation["cutoff"]

        self.converter = Converter(
            cutoff=cutoff,
            device=self.device,
            verbose=verbose,
            skin=skin,
            reference_displacements=None,
            transpose=False,
            report_update=report_update,
            never_update=never_update,
        )

    def calculate(
        self,
        atoms,
    ):

        n = len(atoms)

        converted = self.converter(atoms)
        velocities = torch.tensor(atoms.get_velocities() * units.fs * 1000).to(self.device)

        if self.virials_reference is None:
            r_i = converted.inputs["_positions"].detach().squeeze()
        else:
            r_i = torch.tensor(self.virials_reference.get_positions()).to(self.device)

        model_results = self.model.model(converted.inputs)

        energies = model_results[keys.energies]

        potential_barycenter = torch.sum(r_i.unsqueeze(0) * energies, axis=1)
        hf_potential_term = torch.zeros(3)
        for alpha in range(3):
            tmp = (
                grad(
                    potential_barycenter[:, alpha],
                    converted.inputs["_positions"],
                    retain_graph=True,
                )[0]
                .detach()
                .squeeze()
            )
            hf_potential_term[alpha] = torch.sum(tmp * velocities)

        hf_potential_term = hf_potential_term.cpu().numpy()

        energy = energies.sum()

        gradient = (
            grad(energy, converted.inputs["_positions"], retain_graph=False)[0]
            .detach()
            .squeeze()
        )

        inner = (gradient * velocities).sum(axis=1)
        hf_force_term = (r_i * inner.unsqueeze(1)).sum(axis=0).detach().cpu().numpy()

        self.reporter.step("finalise")
        heat_flux = (hf_potential_term - hf_force_term) / atoms.get_volume()

        self.reporter.done()

        self.results = {
            "heat_flux": heat_flux,
            "heat_flux_force_term": hf_force_term,
            "heat_flux_potential_term": hf_potential_term,
        }
        return self.results


def get_reference_atoms(atoms):
    from ase import Atoms

    if not isinstance(atoms, Atoms):
        comms.talk(f"loading reference positions for virials from {atoms}", full=True)
        from ase.io import read

        atoms = read(atoms, format="aims")

    return atoms
