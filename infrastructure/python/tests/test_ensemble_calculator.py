from unittest import TestCase


class TestEnsembleCalculator(TestCase):
    def test_basic(self):
        import gknet

        models = [gknet.Model() for i in range(5)]
        calc = gknet.gknetEnsembleCalculator(models, stress=True)

        from ase.build import bulk

        atoms = bulk("Ar", cubic=False)
        atoms.set_cell(1.05 * atoms.get_cell(), scale_atoms=True)

        atoms.calc = calc
        atoms.calc.virials = True
        atoms.get_potential_energy()
        self.assertTrue(atoms.calc.virials)
        self.assertTrue("virials" in atoms.calc.results)
        self.assertTrue("energies" in atoms.calc.results)
        self.assertTrue("stress" in atoms.calc.results)
