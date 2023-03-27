import torch

from schnetpack.data.atoms import AtomsConverter
from schnetpack import Properties

from ase import units
from ase.calculators.calculator import Calculator as aseCalculator
from ase.calculators.calculator import all_changes
from ase.constraints import full_3x3_to_voigt_6_stress

from schnetpack.environment import AseEnvironmentProvider

from .model import Model
from .helpers import guess_device_settings, talk


class gknetCalculator(aseCalculator):
    implemented_properties = [
        "energy",
        "forces",
        "stress",
        "stresses",
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
        **kwargs,
    ):
        aseCalculator.__init__(self, **kwargs)

        if not isinstance(model, Model):
            from gknet import load

            model = load(model)

        self.model = model

        self.device, _ = guess_device_settings(device=device)
        talk(f"gknetCalculator will use device {self.device}.")
        self.model.to(self.device)

        self.atoms_converter = AtomsConverter(
            environment_provider=AseEnvironmentProvider(
                cutoff=model.config_representation["cutoff"]
            ),
            device=self.device,
        )

        if virials_reference is not None:
            virials_reference = get_reference(virials_reference, self.device)

        self.virials_reference = virials_reference

        self.energies = energies
        self.stress = stress
        self.virials = virials

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

    def calculate(self, atoms=None, properties=["energy"], system_changes=all_changes):
        aseCalculator.calculate(self, atoms)

        model_inputs = self.atoms_converter(atoms)
        model_results = self.model.model(model_inputs)

        results = {}

        from gknet import keys

        energy = model_results[keys.energy].detach().cpu().numpy()
        results["energy"] = energy.item()

        forces = model_results[keys.forces].detach().cpu().numpy()
        results["forces"] = forces.reshape((len(atoms), 3))

        if self.stress:
            stress = model_results[keys.stress].detach().cpu().numpy().reshape((3, 3))
            results["stress"] = full_3x3_to_voigt_6_stress(stress)

        if self.virials:
            if self.virials_reference is None:
                ref = get_reference(atoms, self.device)
            else:
                ref = self.virials_reference

            virials = compute_virials(
                ref=ref,
                energies=model_results[keys.energies],
                r=model_inputs[Properties.position],
                volume=self.atoms.get_volume(),
            )

            # these are not actually the stresses, but we call
            # them stresses for compatibility
            results["virials"] = virials.detach().cpu().numpy()

            # also write out energies to use for convective heat flux
            energies = model_results[keys.energies].detach().cpu().numpy()
            results["energies"] = energies.reshape(len(atoms))

        if self.energies and "energies" not in results:
            energies = model_results[keys.energies].detach().cpu().numpy()
            results["energies"] = energies.reshape(len(atoms))

        self.results = results

        return results


def compute_virials(ref, energies, r, volume):
    """Compute virials.

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
        rji = ref[i, :, :]  # => [j, a]
        dui_drj = torch.autograd.grad(energies[:, i], r, retain_graph=True)[0].squeeze(
            0
        )  # => [j, b]

        # outer product;
        # see https://discuss.pytorch.org/t/easy-way-to-compute-outer-products/720/5
        virials += rji.unsqueeze(2) * dui_drj.unsqueeze(1)  # => [j, a, b]

    return virials / volume


def get_reference(atoms, device):
    from ase import Atoms

    if not isinstance(atoms, Atoms):
        talk(f"loading reference positions for virials from {atoms}")
        from ase.io import read

        atoms = read(atoms)

    return torch.tensor(
        -atoms.get_all_distances(vector=True, mic=True),
        device=device,
    )
