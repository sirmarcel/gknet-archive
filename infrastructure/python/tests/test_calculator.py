import torch
from unittest import TestCase
from ase.io import Trajectory


from tempdir import Tempdir


class TestCalculator(Tempdir, TestCase):
    def test_basic(self):
        import gknet

        model = gknet.Model()
        calc = gknet.gknetCalculator(model, stress=True)

        from ase.build import bulk

        atoms = bulk("Ar", cubic=True)

        atoms.calc = calc
        atoms.calc.virials = True
        atoms.get_potential_energy()
        self.assertTrue("virials" in atoms.calc.results)
        self.assertTrue("energies" in atoms.calc.results)
        self.assertTrue("stress" in atoms.calc.results)

        atoms.calc.results = {}
        atoms.calc.virials = False
        atoms.get_potential_energy()
        self.assertTrue("virials" not in atoms.calc.results)
        self.assertTrue("energies" not in atoms.calc.results)

        atoms.calc.results = {}
        atoms.calc.stress = False
        atoms.get_potential_energy()
        self.assertTrue("stress" not in atoms.calc.results)
