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

from .unfolder import Unfolder


class UnfoldedHeatFluxCalculator:
    def __init__(
        self,
        model,
        device=None,
        virials_reference=None,
        skin=None,
        skin_unfolder=0.1,
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
        effective_cutoff = cutoff * model.config_representation["n_interactions"]

        if skin is None:
            # unfolder allows movement up to skin/2 in *each direction*,
            # so we pick a skin that corresponds to the 3D distance
            skin = np.sqrt(3) * skin_unfolder

        self.converter_unfolded = Converter(
            cutoff=cutoff,
            device=self.device,
            verbose=verbose,
            skin=skin,
            reference_displacements=None,
            transpose=False,
            report_update=report_update,
            never_update=never_update,
        )

        self.unfolder = Unfolder(
            effective_cutoff,
            skin=skin_unfolder,
            verbose=verbose,
            report_update=report_update,
            never_update=never_update,
        )

        comms.talk(f"cutoff: {cutoff}, effective: {effective_cutoff}")

    def calculate(
        self,
        atoms,
    ):
        self.reporter.start("calculating")

        n = len(atoms)

        self.reporter.step("unfolding")
        unfolded = self.unfolder(atoms)

        if self.verbose:
            comms.talk(f"n: {n}, n unfolded: {len(unfolded.atoms)}")

        self.reporter.step("convert unfolded atoms")
        converted_unfolded = self.converter_unfolded(unfolded.atoms)

        self.reporter.step("prediction unfolded")
        model_results_unfolded = self.model.model(converted_unfolded.inputs)

        self.reporter.step("preparation")
        reference_positions = get_reference_positions(
            self.virials_reference, self.unfolder, converted_unfolded, self.device
        )
        velocities_unfolded = torch.tensor(
            (unfolded.atoms.get_velocities() * units.fs * 1000)
        ).to(self.device)
        r_i = reference_positions.detach().squeeze()[:n]
        energies = model_results_unfolded[keys.energies][:, :n, :]  # energies in uc

        self.reporter.step("virials (potential term)")

        potential_barycenter = torch.sum(r_i.unsqueeze(0) * energies, axis=1)
        hf_potential_term = torch.zeros(3)
        for alpha in range(3):
            tmp = (
                grad(
                    potential_barycenter[:, alpha],
                    converted_unfolded.inputs["_positions"],
                    retain_graph=True,
                )[0]
                .detach()
                .squeeze()
            )
            hf_potential_term[alpha] = torch.sum(tmp * velocities_unfolded)

        hf_potential_term = hf_potential_term.cpu().numpy()

        self.reporter.step("virials (force term)")

        energies_unfolded = model_results_unfolded[keys.energies]
        energy = energies.sum()

        gradient = (
            grad(energy, converted_unfolded.inputs["_positions"], retain_graph=False)[0]
            .detach()
            .squeeze()
        )

        inner = (gradient * velocities_unfolded).sum(axis=1)
        hf_force_term = (
            (reference_positions * inner.unsqueeze(1)).sum(axis=0).detach().cpu().numpy()
        )

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


def get_reference_positions(virials_reference, unfolder, converted_unfolded, device):
    if virials_reference is None:
        reference_positions = converted_unfolded.inputs["_positions"].squeeze()
    else:
        reference_positions = torch.tensor(
            unfolder.unfold(virials_reference).atoms.positions
        ).to(device)

    return reference_positions
