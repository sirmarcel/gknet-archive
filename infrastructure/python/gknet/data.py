import numpy as np
from functools import partial
from pathlib import Path

import torch
from ase.calculators.calculator import PropertyNotImplementedError

from schnetpack.environment import AseEnvironmentProvider
from schnetpack.data.atoms import _convert_atoms

# TODO: replace with comms when we decide to kill legacy support
from vibes.helpers import progressbar

from gknet import keys
from .helpers import stress_to_voigt
from .engine import Stateful

nan = float("nan")


class Data(torch.utils.data.Dataset, Stateful):
    kind = "data"

    def __init__(self, cutoff=5.0, offset=0.0):
        self.offset = offset
        self.cutoff = cutoff

        self.converter = partial(
            _convert_atoms,
            environment_provider=AseEnvironmentProvider(cutoff=cutoff),
        )

        self.data = []

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def _get_config(self):
        return {"offset": self.offset, "cutoff": self.cutoff}

    def _get_state(self):
        return {"data": self.data}

    def _restore(self, state):
        self.data = state["data"]

    def add_atoms(self, iterable, stress=True):
        for atoms in progressbar(iterable, prefix="importing atoms..."):
            self.data.append(
                convert_atoms(atoms, self.converter, self.offset, stress=stress)
            )

    def add_file(self, file, stress=True):
        file = Path(file)
        suffix = file.suffix

        if suffix == ".son" or suffix == ".nc":
            from vibes.trajectory import reader

            self.add_atoms(reader(file), stress=stress)
        elif suffix == ".traj":
            from ase.io import Trajectory

            self.add_atoms(Trajectory(file), stress=stress)

    @property
    def energy(self):
        return torch.tensor([data[keys.energy] for data in self.data]).squeeze()

    @property
    def forces(self):
        # can't meaningfully cast to tensor,
        # as forces might be ragged
        return [data[keys.forces] for data in self.data]

    @property
    def stress(self):
        return torch.tensor([data[keys.stress].tolist() for data in self.data])

    @property
    def stress_voigt(self):
        return stress_to_voigt(self.stress)

    @property
    def var_energy(self):
        return self.energy.var(unbiased=False)

    @property
    def var_forces(self):
        # TODO: generalise to case of non-constant n_atoms 
        # need to construct big array (or compute on the fly)
        forces = torch.cat(self.forces)
        return forces.var(0, unbiased=False)

    @property
    def var_stress(self):
        return self.stress.var(0, unbiased=False)

    @property
    def var_stress_voigt(self):
        return self.stress_voigt.var(0, unbiased=False)


def convert_atoms(atoms, converter, offset, stress=True):
    dictionary = converter(atoms)
    dictionary[keys.energy] = torch.tensor(
        atoms.get_potential_energy() - offset, dtype=torch.float
    ).unsqueeze(0)
    dictionary[keys.forces] = torch.tensor(atoms.get_forces(), dtype=torch.float)

    if stress:
        try:
            dictionary[keys.stress] = torch.tensor(
                atoms.get_stress(voigt=False), dtype=torch.float
            )
        except PropertyNotImplementedError:
            dictionary[keys.stress] = torch.tensor(
                nan * np.zeros((3, 3)), dtype=torch.float
            )

    return torchify_dict(dictionary)


def torchify_dict(data):
    """
    Transform np.ndarrays to torch.tensors.

    """
    torch_properties = {}
    for pname, prop in data.items():

        if prop.dtype in [np.int, np.int32, np.int64]:
            torch_properties[pname] = torch.LongTensor(prop)
        elif prop.dtype in [np.float, np.float32, np.float64]:
            torch_properties[pname] = torch.FloatTensor(prop.copy())
        elif torch.is_tensor(prop):
            torch_properties[pname] = prop
        else:
            raise RuntimeError(
                "Invalid datatype {} for property {}!".format(type(prop), pname)
            )
    return torch_properties
