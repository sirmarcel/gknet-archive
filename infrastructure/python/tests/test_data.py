import torch
from unittest import TestCase
from ase.io import Trajectory

import gknet
from gknet.data import Data


from tempdir import Tempdir


class TestData(Tempdir, TestCase):
    def test_roundtrip(self):
        data = Data()
        data.add_atoms(iterable=Trajectory("md.traj"), stress=True)
        data.save(self.tempdir / "data")
        data2 = gknet.load(self.tempdir / "data")

        for k in data[0].keys():
            self.assertTrue(torch.eq(data[0][k], data2[0][k]).all())

        self.assertTrue(torch.eq(data.energy, data2.energy).all())
        self.assertTrue(torch.eq(data.stress, data2.stress).all())

        data3 = Data()
        data3.add_file("md.traj")
        self.assertTrue(torch.eq(data.energy, data3.energy).all())

        # just test that they don't break
        data.stress_voigt
        data.var_energy
        data.var_forces
        data.var_stress
        data.var_stress_voigt
