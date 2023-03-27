import numpy as np
from collections import namedtuple
from ase import Atoms

from .unfolder_engine import (
    get_unfolding,
    get_replica_offsets,
    get_replicated_positions,
    get_wrap_offsets,
    get_offset_and_box,
    project_onto_planes,
)
from .cell import get_cell

from gknet.experimental.fast_calculator.comms import comms

Unfolded = namedtuple("Unfolded", ("atoms", "unfolding"))
Unfolding = namedtuple(
    "Unfolding",
    (
        "idx",
        "directions",
        "replica_offsets",
        "wrap_offsets",
        "cell",
        "shift_offset",
        "bounding_box",
    ),
)


class Unfolder:
    """Unfolder

    Unfolds periodic boundaries up to a given cutoff, caching the
    computation of which atoms to replicate where with some tolarance.

    The end result is a non-periodic system where the first N positions
    correspond to the N atoms in the unit cell, and the rest are the replicas
    in various directions, so that the original N atoms see the exact same
    neighbours, with the same distances, but now explicitly rather than via
    the minimum image convention.

    We make two basic assumptions:
    - The cutoff is smaller than half the smallest unit cell vector,
    - The unit cell is orthombic, i.e. a cube with different side lenghts.

    The former should not break the algorithm, but leads to atoms "seeing"
    themselves which might be unexpected (and breaks the unit test). The algorithm
    implemented here is also intended for the case where the cutoff is substantially
    smaller than the unit cell, because otherwise, we might as well just replicate the
    whole (or maybe half) unit cell 3x3x3 times and be done with it.

    The latter is just for convenience, allowing us to avoid transforming into
    fractional coordinates. A general implementation would simply work in f.c.,
    using the exact same principles, except that there would be different cutoffs
    in each cell direction.

    In this implementation, we decompose the task into three steps:
    (a) Wrapping atoms that are outside the unit cell back,
    (b) Figuring out which atoms to replicate in which direction,
    (c) Actually doing the replication.

    The advantage of this split is that we can cache the result of (a) and (b),
    similar to neighborlist generation: We internally use `eff_cutoff = cutoff + skin`
    and only re-compute the "Unfolding instructions" when atoms move more than `skin/2`.

    We need to include the wrapping operation in this to avoid atoms jumping: if
    that happens, we break caching of the neighborlist, which is very costly to compute
    with ase. By only re-doing the wrapping if the atoms move too much, we avoid them
    hopping around when they repeatedly cross the boundary during dynamics.

    The result of (a) are simple offsets to be added to each position to bring it back
    into the unit cell.

    The result of (b) is an index array that tells us which replica is which original
    atom in the unit call, and another array that tells us in which direction said replica
    is supposed to be taken.

    For (c) we then simply execute these instructions.

    Then we need to put together a new Atoms object, and off we go.

    For more details on the algorithm, see `unfolder_engine.py`.

    """

    def __init__(
        self, cutoff, skin=0.0, verbose=False, report_update=False, never_update=False
    ):
        self.cutoff = cutoff
        self.skin = skin

        self.atoms = None
        self.reporter = comms.reporter(silent=(not verbose))

        self.report_update = report_update

        # hack to circumentvent caching for testing/benchmarking
        self.never_update = never_update
        if self.never_update:
            comms.talk(
                "using Unfolder in testing mode: cache will never invalidate but results may be wrong",
                full=True,
            )

    def __call__(self, atoms, shift=True):
        self.reporter.start("unfolding")

        if self.needs_update(atoms):
            self.atoms = atoms.copy()
            self.reporter.step("update")
            if self.report_update:
                comms.talk("updating unfolding")
            self.update()

        self.reporter.step("replicating")
        unfolded = self.unfold(atoms, shift=shift)

        self.reporter.done()
        return unfolded

    def unfold(self, atoms, shift=True):
        atoms_unfolded = self._unfold(atoms)

        if shift:
            atoms_unfolded.positions += self.unfolding.shift_offset[None, :]
            atoms_unfolded.set_cell(self.unfolding.bounding_box)

        return Unfolded(atoms_unfolded, self.unfolding)

    def _unfold(self, atoms):
        original_positions = atoms.get_positions()
        wrapped_positions = original_positions + self.unfolding.wrap_offsets
        replicated_positions = get_replicated_positions(
            wrapped_positions,
            self.unfolding.idx,
            self.unfolding.directions,
            self.unfolding.replica_offsets,
        )
        all_positions = np.concatenate((wrapped_positions, replicated_positions))
        all_numbers = np.concatenate((atoms.numbers, atoms.numbers[self.unfolding.idx]))
        all_velocities = np.concatenate(
            (atoms.get_velocities(), atoms.get_velocities()[self.unfolding.idx])
        )

        atoms_unfolded = Atoms(
            positions=all_positions,
            numbers=all_numbers,
            velocities=all_velocities,
            pbc=False,
        )

        return atoms_unfolded

    def update(self):
        # todo: consider that if this happens w/o a corresponding
        # update of the nl, and in the freak chance that N doesn't
        # change, AND this doesn't invalidate the nl by itself,
        # then we can get a wrong nl... very unlikely, tho
        cell = get_cell(self.atoms.get_cell())

        original_positions = self.atoms.get_positions()
        wrap_offsets = get_wrap_offsets(original_positions, cell)
        wrapped_positions = original_positions + wrap_offsets

        idx, directions = get_unfolding(
            wrapped_positions, cell, self.cutoff + self.skin
        )

        replica_offsets = get_replica_offsets(cell)

        shift_offset, bounding_box = get_offset_and_box(cell, self.cutoff + self.skin)

        self.unfolding = Unfolding(
            idx,
            directions,
            replica_offsets,
            wrap_offsets,
            cell,
            shift_offset,
            bounding_box,
        )

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

        before = project_onto_planes(my_positions, self.unfolding.cell)
        after = project_onto_planes(new_positions, self.unfolding.cell)
        changes = np.abs(before - after)

        # factor 0.5 to treat the following situation:
        # atom a at L-c-s, atom b at 0; move by +s and -s respectively
        # -> they have mic. distance of c-s, but a is not replicated so b can't see it
        return changes.max() >= 0.5 * self.skin
