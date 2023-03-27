import torch
from collections import namedtuple
from schnetpack.data.atoms import AtomsConverter
from schnetpack.environment import AseEnvironmentProvider, BaseEnvironmentProvider

from vibes.helpers.utils import Timer

from gknet.helpers import guess_device_settings, talk

from .comms import comms
from .transpose import get_transpose_idx

Converted = namedtuple("Converted", ["inputs", "neighborhood"])
Neighborhood = namedtuple(
    "Neighborhood", ["idx", "offset", "reference_displacements", "transpose_idx"]
)


class Converter:
    def __init__(
        self,
        cutoff,
        device=None,
        skin=0.3,
        verbose=False,
        reference_displacements=None,
        transpose=False,
        report_update=False,
        never_update=False,
    ):
        self.skin = skin
        self.cutoff = cutoff
        self.device, _ = guess_device_settings(device=device)
        self.reporter = comms.reporter(silent=(not verbose))
        self.transpose = transpose

        self.reference_displacements = reference_displacements

        self.environment_provider = AseEnvironmentProvider(
            cutoff=(self.cutoff + self.skin)
        )

        self.atoms = None
        self.neighborhood = None

        comms.talk("using corrected skin converter")

        self.report_update = report_update
        self.never_update = never_update
        if self.never_update:
            comms.talk(
                "using Converter in testing mode: cache will never invalidate but results may be wrong",
                full=True,
            )

    def __call__(self, atoms):
        self.reporter.start("converting atoms")
        if self.needs_update(atoms):
            self.reporter.step("updating neighborhood")
            self.atoms = atoms.copy()
            if self.report_update:
                comms.talk("updating neighborlist")
            self.neighborhood = self.get_neighborhood(self.atoms)

        self.reporter.step("atoms to schnetpack")
        converter = AtomsConverter(
            environment_provider=FakeEnvironmentProvider(self.neighborhood),
            device=self.device,
        )
        inputs = converter(atoms)

        self.reporter.done()
        return Converted(inputs, self.neighborhood)

    def get_neighborhood(self, atoms):
        idx, offset = self.environment_provider.get_environment(atoms)

        if self.reference_displacements is not None:
            reference_displacements = get_reference_displacements(
                self.reference_displacements, idx
            ).to(self.device)
        else:
            reference_displacements = None

        if self.transpose:
            transpose_idx = get_transpose_idx(idx)
        else:
            transpose_idx = None

        return Neighborhood(idx, offset, reference_displacements, transpose_idx)

    def needs_update(self, atoms):
        if self.atoms is None:
            return True
        elif self.never_update:
            return False
        else:
            return self._needs_update(atoms)

    def _needs_update(self, atoms):
        if (
            (self.atoms.get_cell() != atoms.get_cell()).any()
            or (self.atoms.get_pbc() != atoms.get_pbc()).any()
            or self.atoms.get_positions().shape != atoms.get_positions().shape
            or (self.atoms.get_atomic_numbers() != atoms.get_atomic_numbers()).any()
        ):
            return True

        my_positions = self.atoms.get_positions()
        new_positions = atoms.get_positions()
        return ((my_positions - new_positions) ** 2).sum(1).max() > (
            0.5 * self.skin
        ) ** 2


class FakeEnvironmentProvider(BaseEnvironmentProvider):
    def __init__(self, neighborhood):
        self.neighborhood = neighborhood

    def get_environment(self, atoms):
        return self.neighborhood.idx, self.neighborhood.offset


def get_reference_displacements(reference_displacements, idx):
    # res[i, j] = reference_displacements[i, idx[i, j]]

    idx_i = torch.arange(reference_displacements.shape[0], dtype=torch.long).unsqueeze(
        -1
    )
    idx_j = idx

    return reference_displacements[idx_i, idx_j, :]
