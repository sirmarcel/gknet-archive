import numpy as np
from unittest import TestCase

from helpers import compare_distances


def get_schnet_distances(inputs):
    from schnetpack.nn.neighbors import atom_distances
    from schnetpack import Properties

    positions = inputs[Properties.R]
    cell = inputs[Properties.cell]
    cell_offset = inputs[Properties.cell_offset]
    neighbors = inputs[Properties.neighbors]
    neighbor_mask = inputs[Properties.neighbor_mask]

    return atom_distances(
        positions,
        neighbors,
        cell=cell,
        cell_offsets=cell_offset,
        neighbor_mask=neighbor_mask,
    )


def random_movements(n, amount):
    directions = np.random.random((n, 3))
    directions /= np.sqrt(np.sum(directions ** 2, axis=1))[:, None]

    magnitudes = np.random.random(n) * amount

    return directions * magnitudes[:, None]


class TestConverter(TestCase):
    def test_basic(self):
        from ase.build import bulk

        atoms = bulk("Ar", cubic=True) * [5, 5, 5]

        from gknet.experimental.fast_calculator.converter import Converter

        converter = Converter(cutoff=5.0, skin=0.5)

        converted = converter(atoms)

        assert not converter.needs_update(atoms)

        updated = atoms.get_positions()
        updated[0, 0] += 0.2
        atoms.set_positions(updated)
        assert not converter.needs_update(atoms)

        updated = atoms.get_positions()
        updated[0, 0] += 0.6
        atoms.set_positions(updated)
        assert converter.needs_update(atoms)

        assert converter.needs_update(atoms * [2, 2, 2])

    def test_distances(self):
        from ase import Atoms
        from gknet.experimental.fast_calculator.converter import Converter

        n = 250
        cutoff = 0.39
        skin = 0.1
        spread = 0.3
        cell = np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]])

        converter = Converter(cutoff=cutoff, skin=skin)

        # generate positions that are slightly outside the u.c.,
        # just in case there are surprises with wrapping
        positions = np.random.random((n, 3))
        positions[:, 0] = (1.0 + 2 * spread) * positions[:, 0] - spread
        positions[:, 1] = (2.0 + 2 * spread) * positions[:, 1] - spread
        positions[:, 2] = (3.0 + 2 * spread) * positions[:, 2] - spread

        # test: does this work at all? do we get the same distances?
        atoms = Atoms(positions=positions, cell=cell, pbc=True)
        converted = converter(atoms)

        schnet_distances = get_schnet_distances(converted.inputs)[0].numpy()
        ase_distances = atoms.get_all_distances(mic=True).astype(np.float32)

        for i in range(len(atoms)):
            compare_distances(schnet_distances[i], ase_distances[i], cutoff, atol=1e-6)

        # test: move a little bit (don't trigger recompute)
        atoms2 = atoms.copy()
        atoms2.positions += random_movements(len(atoms), 0.5 * skin)

        self.assertFalse(converter._needs_update(atoms2))
        converted = converter(atoms2)
        schnet_distances = get_schnet_distances(converted.inputs)[0].numpy()
        ase_distances = atoms2.get_all_distances(mic=True).astype(np.float32)

        for i in range(len(atoms)):
            compare_distances(schnet_distances[i], ase_distances[i], cutoff, atol=1e-6)

        # test: move a little bit more (trigger recompute)
        atoms3 = atoms2.copy()
        atoms3.positions += random_movements(len(atoms), 0.5 * skin)

        self.assertTrue(converter._needs_update(atoms3))
        converted = converter(atoms3)
        schnet_distances = get_schnet_distances(converted.inputs)[0].numpy()
        ase_distances = atoms3.get_all_distances(mic=True).astype(np.float32)

        for i in range(len(atoms)):
            compare_distances(schnet_distances[i], ase_distances[i], cutoff, atol=1e-6)
