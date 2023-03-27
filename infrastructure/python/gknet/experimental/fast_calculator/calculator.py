import torch
from torch.autograd import grad
import numpy as np

from schnetpack import Properties

from ase import units
from ase.calculators.calculator import Calculator as aseCalculator
from ase.calculators.calculator import all_changes
from ase.constraints import full_3x3_to_voigt_6_stress

from vibes.helpers import Timer

from gknet.model import Model
from gknet.helpers import guess_device_settings, talk
from gknet import keys

from .converter import Converter
from .model import Model
from .comms import comms


class fastCalculator(aseCalculator):
    implemented_properties = [
        "energy",
        "forces",
        "stress",
        "energies",
    ]

    def __init__(
        self,
        model,
        device=None,
        stress=False,
        energies=False,
        virials=False,
        virials_reference=None,
        verbose=False,
        skin=0.3,
        hardy=False,
        fan=False,
        fan_mpnn=False,
        symmetrize_derivatives=False,
        transpose_derivatives=False,
        barycenter=False,
        heat_flux=False,
        report_update=False,
        never_update=False,
        **kwargs,
    ):
        aseCalculator.__init__(self, **kwargs)

        self.verbose = verbose
        self.reporter = comms.reporter(silent=(not self.verbose))

        if not isinstance(model, Model):
            from torch import load

            if self.verbose:
                comms.talk(f"loading model from {model}")

            tmp = torch.load(model)
            model = Model.from_config(tmp["config"]["model"])
            model.restore(tmp["state"])

        self.model = model
        self.model.training = False  # avoid building graph for second-order derivatives
        self.model.return_pairwise = virials

        self.device, _ = guess_device_settings(device=device)
        if self.verbose:
            comms.talk(f"fastCalculator will use device {self.device}.")
        self.model.to(self.device)

        if virials_reference is not None:
            if self.verbose:
                comms.talk("using fixed reference positions for virials")

            virials_reference, barycenter_reference = get_reference(virials_reference)

        else:
            barycenter_reference = None

        self.virials_reference = virials_reference
        self.barycenter_reference = barycenter_reference

        self.energies = energies
        self.stress = stress
        self.virials = virials
        self.heat_flux = heat_flux

        self.hardy = hardy
        if self.hardy:
            comms.talk(f"using hardy virials")

        self.fan = fan
        self.fan_mpnn = fan_mpnn
        if self.fan:
            comms.talk("using fan et al. virials")
            if self.fan_mpnn:
                comms.talk("... with MPNN correction!")

        self.barycenter = barycenter
        if self.barycenter:
            comms.talk(f"computing barycenter properties")

        self.symmetrize_derivatives = symmetrize_derivatives

        if self.symmetrize_derivatives and not (self.fan or self.hardy):
            comms.talk("symmetrizing derivatives for virials!")

        self.transpose_derivatives = transpose_derivatives
        if self.transpose_derivatives and not (self.fan or self.hardy):
            comms.talk("transposing derivatives for virials!")

        need_transpose = (
            self.fan or self.symmetrize_derivatives or self.transpose_derivatives
        )

        self.converter = Converter(
            cutoff=model.config_representation["cutoff"],
            device=self.device,
            verbose=verbose,
            skin=skin,
            reference_displacements=self.virials_reference,
            transpose=need_transpose,
            report_update=report_update,
            never_update=never_update,
        )

    @property
    def stress(self):
        return self._stress

    @stress.setter
    def stress(self, compute_stress):
        if compute_stress:
            self.model.stress = True
            self._stress = True
        else:
            self.model.stress = False
            self._stress = False

    @property
    def virials(self):
        return self.model.return_pairwise

    @virials.setter
    def virials(self, compute_virials):
        self.model.return_pairwise = compute_virials

    def calculate(
        self,
        atoms=None,
        properties=None,
        system_changes=None,
        debug=False,
        **kwargs,
    ):
        aseCalculator.calculate(self, atoms)

        self.reporter.start("calculating")

        converted = self.converter(atoms)

        self.reporter.step("prediction")
        model_results = self.model.model(converted.inputs)

        self.reporter.step("collect results")
        results = {}

        energy = model_results[keys.energy].detach().cpu().numpy()
        results["energy"] = energy.item()

        forces = model_results[keys.forces].detach().cpu().numpy()
        results["forces"] = forces.reshape((len(atoms), 3))

        if self.stress:
            stress = model_results[keys.stress].detach().cpu().numpy().reshape((3, 3))
            results["stress"] = full_3x3_to_voigt_6_stress(stress)

        if self.virials and not self.hardy and not self.fan:
            self.reporter.step("fast virials (prep)")

            r_ij = converted.inputs["pairwise_distances"]

            du_drij = grad(
                model_results[keys.energy],
                r_ij,
                retain_graph=debug,
            )[0]
            du_drij = du_drij.detach().squeeze()

            mask = converted.inputs["_neighbor_mask"].squeeze()

            if self.transpose_derivatives:
                du_drij = (
                    du_drij[
                        converted.neighborhood.transpose_idx[:, :, 0],
                        converted.neighborhood.transpose_idx[:, :, 1],
                    ]
                    * mask
                )

            if self.symmetrize_derivatives:
                du_drji = (
                    du_drij[
                        converted.neighborhood.transpose_idx[:, :, 0],
                        converted.neighborhood.transpose_idx[:, :, 1],
                    ]
                    * mask
                )
                du_drij = 0.5 * (du_drij + du_drji)

            r_ij = r_ij.detach().squeeze()
            hatr_ij = (
                converted.inputs["pairwise_normalized_displacements"].detach().squeeze()
            )

            if self.virials_reference is not None:
                vecr_ij = converted.neighborhood.reference_displacements
                if self.verbose:
                    comms.talk("using fixed reference positions for virials")
            else:
                vecr_ij = None

            self.reporter.step("fast virials")
            virials = compute_virials(
                du_drij=du_drij,
                r_ij=r_ij,
                hatr_ij=hatr_ij,
                volume=self.atoms.get_volume(),
                vecr_ij=vecr_ij,
            )
            if debug:
                comms.warn("debug enabled, dumping results")
                self.reporter.done()
                return {
                    "converted": converted,
                    "model_results": model_results,
                    "results": results,
                    "du_drij": du_drij,
                    "r_ij": r_ij,
                    "hatr_ij": hatr_ij,
                    "virials": virials,
                    "virials_reference": self.virials_reference,
                }

            results["virials"] = virials.detach().cpu().numpy()
            self.reporter.finish_step()

        if self.virials and self.hardy:
            self.reporter.step("hardy virials (prep)")
            if self.virials_reference is not None:
                ref = self.virials_reference
            else:
                ref = get_reference(atoms)[0]

            self.reporter.step("hardy virials", spin=False)
            virials = compute_hardy_virials(
                ref=ref.to(self.device),
                energies=model_results[keys.energies],
                r=converted.inputs[Properties.position],
                volume=self.atoms.get_volume(),
                reporter=self.reporter,
            )

            results["virials"] = virials.detach().cpu().numpy()

            self.reporter.finish_step()

        if self.virials and self.fan:
            from .fan import compute_fan_virials

            self.reporter.step("fan virials (prep)")

            if self.virials_reference is not None:
                ref = self.virials_reference
            else:
                ref = get_reference(atoms)[0]

            hatr_ij = (
                converted.inputs["pairwise_normalized_displacements"].detach().squeeze()
            )

            self.reporter.step("fan virials", spin=False)
            virials = compute_fan_virials(
                ref=ref.to(self.device),
                energies=model_results[keys.energies],
                r_ij=converted.inputs["pairwise_distances"],
                idx=converted.neighborhood.idx,
                hatr_ij=hatr_ij,
                volume=self.atoms.get_volume(),
                reporter=self.reporter,
                transpose_idx=converted.neighborhood.transpose_idx,
                mask=converted.inputs["_neighbor_mask"].squeeze(),
                full=self.fan_mpnn,
            )

            results = {**results, **virials}
            if not self.fan_mpnn:
                results["virials"] = virials["fan_virials"]
            else:
                results["virials"] = virials["fan_virials_mpnn"]

        if self.barycenter:
            from .barycenter import compute_barycenter

            energies = model_results[keys.energies]
            positions = converted.inputs[Properties.position]
            forces = model_results[keys.forces].detach().squeeze()
            velocities = torch.tensor(atoms.get_velocities() * units.fs * 1000).to(
                self.device
            )
            volume = atoms.get_volume()

            if self.barycenter_reference is not None:
                r0_j, r0_j_pot, r0_j_kin = compute_barycenter(
                    reference=self.barycenter_reference.to(self.device),
                    energies=energies,
                    positions=positions,
                    forces=forces,
                    velocities=velocities,
                    volume=volume,
                )

                results["barycenter_r0_heat_flux"] = r0_j
                results["barycenter_r0_heat_flux_pot"] = r0_j_pot
                results["barycenter_r0_heat_flux_kin"] = r0_j_kin

            rt_j, rt_j_pot, rt_j_kin = compute_barycenter(
                reference=positions.detach().squeeze(),
                energies=energies,
                positions=positions,
                forces=forces,
                velocities=velocities,
                volume=volume,
            )

            results["barycenter_rt_heat_flux"] = rt_j
            results["barycenter_rt_heat_flux_pot"] = rt_j_pot
            results["barycenter_rt_heat_flux_kin"] = rt_j_kin

        if (self.energies or self.virials) and "energies" not in results:
            energies = model_results[keys.energies].detach().cpu().numpy()
            results["energies"] = energies.reshape(len(atoms))

        if self.heat_flux:
            vs = atoms.get_velocities() * units.fs * 1000
            fluxes = np.squeeze(results["virials"] @ vs[:, :, None])
            heat_flux = fluxes.sum(axis=0)
            results["heat_flux"] = heat_flux

        self.results = results

        self.reporter.done()

        if debug:  # but not virials
            comms.warn("debug enabled, dumping results")

            return {
                "converted": converted,
                "model_results": model_results,
                "results": results,
            }

        return results


def compute_virials(du_drij, r_ij, hatr_ij, volume, vecr_ij=None):
    """Compute virials."""

    # derivative wrt displacement vectors
    du_dvecrij = du_drij.unsqueeze(-1) * hatr_ij

    # displacment vectors
    if vecr_ij is None:
        vecr_ij = r_ij.unsqueeze(-1) * hatr_ij

    # outer product across cartesian dimensions
    # (order is arbitrary; it's symmetric anyway)
    # sign also doesn't matter, but the derivation is slightly more
    # consistent with the -1!
    virials = -1.0 * vecr_ij.unsqueeze(-1) * du_dvecrij.unsqueeze(-2)

    # sum over j
    virials = torch.sum(virials, axis=1)

    return virials / volume


def compute_hardy_virials(ref, energies, r, volume, reporter):
    """Compute virials with the Hardy formula

    In particular, we compute:

        sum_i r_ji (d U_i)/(d r_j); i.e. a [j, 3] tensor.

    Args:
        ref: [i, j, a] Reference positions (should be pairwise mic distance vectors)
        energies: [1, i, 1] Atomic energies
        r: [1, i, a] Positions (must be the tensor used to compute ui, we need gradients)
        volume: scalar, Volume of unit cell (vibes expects intensive virials)

    Note that this is not vectorised across a batch; the calculator
    does one structure at a time anyways.

    """

    virials = torch.zeros(energies.shape[1], 3, 3, device=energies.device)
    for i in range(energies.shape[1]):
        reporter.tick(f"(atom {i})")
        rji = -1.0 * ref[i, :, :]  # => [j, a] // sign due to convention
        dui_drj = torch.autograd.grad(energies[:, i], r, retain_graph=True)[0].squeeze(
            0
        )  # => [j, b]

        # outer product;
        # see https://discuss.pytorch.org/t/easy-way-to-compute-outer-products/720/5
        virials += rji.unsqueeze(2) * dui_drj.unsqueeze(1)  # => [j, a, b]

    return virials / volume


def get_reference(atoms):
    from ase import Atoms

    if not isinstance(atoms, Atoms):
        comms.talk(f"loading reference positions for virials from {atoms}", full=True)
        from ase.io import read

        atoms = read(atoms, format="aims")

    return torch.tensor(atoms.get_all_distances(vector=True, mic=True)), torch.tensor(
        atoms.get_positions()
    )
