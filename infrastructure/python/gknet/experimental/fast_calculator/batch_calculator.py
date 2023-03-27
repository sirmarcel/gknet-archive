import torch
from torch.autograd import grad

from schnetpack import Properties
from schnetpack.data.loader import _collate_aseatoms

from ase.constraints import full_3x3_to_voigt_6_stress

from gknet.model import Model
from gknet.helpers import guess_device_settings, talk
from gknet import keys

from .converter import Converter
from .model import Model
from .comms import comms


class batchCalculator:
    def __init__(
        self,
        model,
        device=None,
        energy=False,
        forces=False,
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
        **kwargs,
    ):

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
        self.model.stress = stress

        self.device, _ = guess_device_settings(device=device)
        if self.verbose:
            comms.talk(f"batchCalculator will use device {self.device}.")
        self.model.to(self.device)

        if virials_reference is not None:
            if self.verbose:
                comms.talk("using fixed reference positions for virials")

            virials_reference, barycenter_reference = get_reference(virials_reference)

        else:
            barycenter_reference = None

        self.virials_reference = virials_reference
        self.barycenter_reference = barycenter_reference

        self.energy = energy
        self.forces = forces
        self.energies = energies
        self.stress = stress
        self.virials = virials

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
        )

    def calculate(self, atomss):

        self.reporter.start("calculating")

        all_converted = [self.converter(atoms) for atoms in atomss]

        squeezed_inputs = []
        for converted in all_converted:
            tmp = {}
            for key, value in converted.inputs.items():
                tmp[key] = value.squeeze(0)

            squeezed_inputs.append(tmp)

        inputs = _collate_aseatoms(squeezed_inputs)

        self.reporter.step("prediction")
        model_results = self.model.model(inputs)

        self.reporter.step("collect results")
        results = {}

        if self.energy:
            results["energy"] = (
                model_results[keys.energy].detach().squeeze(-1).cpu().numpy()
            )

        if self.forces:
            results["forces"] = model_results[keys.forces].detach().cpu().numpy()

        if self.stress:
            stress = model_results[keys.stress].detach().cpu().numpy()
            results["stress"] = full_3x3_to_voigt_6_stress(stress)

        if self.virials and self.hardy:
            self.reporter.step("hardy virials (prep)")
            if self.virials_reference is not None:
                n_batch = len(atomss)
                n_atoms = len(atomss[0])
                ref = self.virials_reference.expand(n_batch, n_atoms, n_atoms, 3)
            else:
                ref = torch.cat(
                    [get_reference(atoms)[0].unsqueeze(0) for atoms in atomss]
                )

            volume = torch.tensor([atoms.get_volume() for atoms in atomss])

            self.reporter.step("hardy virials", spin=False)
            virials = compute_hardy_virials(
                ref=ref.to(self.device),
                energies=model_results[keys.energies],
                r=inputs[Properties.position],
                volume=volume.to(self.device),
                reporter=self.reporter,
            )

            results["virials"] = virials.detach().cpu().numpy()

            self.reporter.finish_step()

        if self.virials and not self.hardy:
            raise NotImplementedError("only hardy flux supported at the moment")

        if self.energies:
            results["energies"] = (
                model_results[keys.energies].detach().squeeze(-1).cpu().numpy()
            )

        self.reporter.done()

        return results


def compute_hardy_virials(ref, energies, r, volume, reporter):
    """Compute virials with the Hardy formula

    In particular, we compute:

        sum_i r_ji (d U_i)/(d r_j); i.e. a [j, 3] tensor.

    Args:
        ref: [i, j, a] Reference positions (should be pairwise mic distance vectors)
        energies: [1, i, 1] Atomic energies
        r: [1, i, a] Positions (must be the tensor used to compute ui, we need gradients)
        volume: scalar, Volume of unit cell (vibes expects intensive virials)


    """

    virials = torch.zeros(
        energies.shape[0], energies.shape[1], 3, 3, device=energies.device
    )
    for i in range(energies.shape[1]):
        reporter.tick(f"(atom {i})")
        rji = -1.0 * ref[:, i, :, :]  # => [batch, j, a] // sign due to convention
        dui_drj = torch.autograd.grad(
            energies[:, i],
            r,
            retain_graph=True,
            grad_outputs=torch.ones_like(energies[:, i]),
        )[
            0
        ]  # => [batch, j, b]

        # outer product;
        # see https://discuss.pytorch.org/t/easy-way-to-compute-outer-products/720/5
        virials += rji.unsqueeze(-1) * dui_drj.unsqueeze(-2)  # => [batch, j, a, b]

    # clown face emoji
    return virials / volume.unsqueeze(1).unsqueeze(1).unsqueeze(1)


def get_reference(atoms):
    from ase import Atoms

    if not isinstance(atoms, Atoms):
        comms.talk(f"loading reference positions for virials from {atoms}", full=True)
        from ase.io import read

        atoms = read(atoms, format="aims")

    return torch.tensor(atoms.get_all_distances(vector=True, mic=True)), torch.tensor(
        atoms.get_positions()
    )
