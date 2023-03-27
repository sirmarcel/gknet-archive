from unittest import TestCase

import numpy as np
from ase import Atoms
from gknet.experimental.unfolded_heatflux.unfolder import Unfolder

from helpers import compare_distances


def compare_all_distances(atoms, unfolded, cutoff):
    dist = atoms.get_all_distances(mic=True)
    unfolded_dist = unfolded.atoms.get_all_distances(mic=True)

    for i in range(len(atoms)):
        compare_distances(dist[i], unfolded_dist[i], cutoff)


def compare_all_distances_with_nl(atoms, unfolded, cutoff):
    """Slower, but treats multiple replicas"""
    from ase.neighborlist import neighbor_list

    dist, idx_dist = neighbor_list("di", atoms, cutoff, self_interaction=False)
    unfolded_dist, idx_unfolded_dist = neighbor_list(
        "di", unfolded.atoms, cutoff, self_interaction=False
    )

    for i in range(len(atoms)):
        a = dist[np.where(idx_dist == i)]
        b = unfolded_dist[np.where(idx_unfolded_dist == i)]
        compare_distances(a, b, cutoff)


def perturb_along_normal(atoms, spread, basis=0):
    from gknet.experimental.unfolded_heatflux.cell import get_cell

    atoms = atoms.copy()

    cell = get_cell(atoms.get_cell())
    direction = cell.normals[basis]
    positions = atoms.get_positions()

    randoms = np.random.random(len(atoms)) * 2 * spread - spread
    positions += randoms[:, None] * direction

    atoms.set_positions(positions)

    return atoms


def perturb_random(atoms, spread):
    atoms = atoms.copy()
    atoms.positions += np.random.random((len(atoms), 3)) * spread - spread / 2

    return atoms


class TestUnfolder(TestCase):
    def test_distances(self):
        for cutoff, cell in [
            (0.29, np.array([[5.1, 0.0, 0.0], [-2.5, 4.42, 0.0], [0.0, 0.0, 13.0]])),
            (0.39, np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]])),
        ]:
            n = 250
            skin = 0.1
            spread = 0.1

            unfolder = Unfolder(cutoff=cutoff, skin=skin)

            # generate positions that are slightly outside the u.c.
            # (this case is very common in MD, and we need to treat
            # it in a reasonable way!)
            positions = np.random.random((n, 3)) * (1 + 2 * spread) - spread

            # test: does this work at all? do we get the same distances?
            atoms = Atoms(scaled_positions=positions, cell=cell, pbc=True)
            unfolded = unfolder(atoms)

            compare_all_distances(atoms, unfolded, cutoff)

            # test: move atoms w/o triggering recomputation
            # case 1: tiny random changes
            atoms2 = perturb_random(atoms, 0.05)
            self.assertFalse(unfolder._needs_update(atoms2))

            # case 2: change orthogonal to surfaces
            for i in range(3):
                atoms2 = perturb_along_normal(atoms, skin / 2, basis=i)
                self.assertFalse(unfolder._needs_update(atoms2))

            # now we just check that things work
            atoms2 = perturb_along_normal(atoms, skin / 2, basis=0)
            unfolded2 = unfolder(atoms2)
            compare_all_distances(atoms2, unfolded2, cutoff)

            # test: move atoms *further*, triggering recomputation
            atoms3 = perturb_along_normal(atoms2, skin / 2, basis=0)
            atoms3 = perturb_along_normal(atoms3, skin / 2, basis=1)
            self.assertTrue(unfolder._needs_update(atoms3))

            unfolded3 = unfolder(atoms3)
            compare_all_distances(atoms3, unfolded3, cutoff)

    def test_large_cutoff(self):
        n = 10
        skin = 0.1
        spread = 0.1
        cutoff = 0.89
        cell = np.eye(3)
        unfolder = Unfolder(cutoff=cutoff, skin=skin)
        positions = np.random.random((n, 3)) * (1 + 2 * spread) - spread

        atoms = Atoms(scaled_positions=positions, cell=cell, pbc=True)
        unfolded = unfolder(atoms)

        compare_all_distances_with_nl(atoms, unfolded, cutoff)


class TestUnfolderEngine(TestCase):
    def test_get_wrap_offsets(self):
        from gknet.experimental.unfolded_heatflux.unfolder_engine import (
            get_wrap_offsets,
        )
        from gknet.experimental.unfolded_heatflux.cell import get_cell

        positions = np.array(
            [[0.5, 0, 0], [-0.2, 0, 0], [-0.05, 0, 0], [1.05, 0, 0], [1.2, 0, 0]]
        )
        cell = np.eye(3)
        cell = get_cell(cell)
        offsets = get_wrap_offsets(positions, cell)

        should = positions % 1.0

        np.testing.assert_allclose(positions + offsets, should)

    def test_get_wrap_offsets_non_orthorhombic(self):
        from ase.geometry import wrap_positions
        from gknet.experimental.unfolded_heatflux.unfolder_engine import (
            get_wrap_offsets,
        )
        from gknet.experimental.unfolded_heatflux.cell import get_cell

        scaled_positions = np.random.random((10, 3)) * 1.2 - 0.1
        cell = np.array([[1, 0, 0], [1, 1, 0], [0, 0, 1]])
        positions = np.dot(scaled_positions, cell)

        cell = get_cell(cell)
        offsets = get_wrap_offsets(positions, cell)

        should = wrap_positions(positions, cell.basis, eps=0)

        np.testing.assert_allclose(positions + offsets, should)

    def test_shift_into_box(self):
        from gknet.experimental.unfolded_heatflux.cell import get_cell
        from gknet.experimental.unfolded_heatflux.unfolder_engine import (
            get_offset_and_box,
            project_onto_planes,
        )

        for cutoff, cell in [
            (0.29, np.array([[5.1, 0.0, 0.0], [-2.5, 4.42, 0.0], [0.0, 0.0, 13.0]])),
            (0.39, np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]])),
        ]:

            spread = 0.1
            n = 250
            cell = get_cell(cell)

            positions = np.random.random((n, 3)) * (1 + 2 * spread) - spread
            og = Atoms(scaled_positions=positions, cell=cell.basis, pbc=True)

            unfolder = Unfolder(cutoff=cutoff)
            atoms_with_shift = unfolder(og).atoms
            atoms_without_shift = unfolder.unfold(og, shift=False).atoms

            scaled_positions = atoms_without_shift.get_scaled_positions(wrap=False)
            self.assertTrue((scaled_positions < 0).any())
            self.assertTrue((scaled_positions > 1).any())

            scaled_positions = atoms_with_shift.get_scaled_positions(wrap=False)
            self.assertTrue((scaled_positions >= 0).all())
            self.assertTrue((scaled_positions <= 1).all())
