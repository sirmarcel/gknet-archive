from unittest import TestCase

import numpy as np
from ase.build import bulk

from gknet.experimental.unfolded_heatflux import UnfoldedHeatFluxCalculator


class TestUnfoldedHeatFluxCalculator(TestCase):
    def test_fire(self):
        from gknet.experimental.fast_calculator.model import Model
        for atoms in (bulk("Ar", cubic=True) * [5, 5, 5], bulk("Ar", cubic=False) * [5, 5, 5]):
            atoms.set_velocities(np.random.random((len(atoms), 3)))

            calc = UnfoldedHeatFluxCalculator(Model())

            res = calc.calculate(atoms)
            self.assertEqual(res["heat_flux"].shape, (3,))

            calc = UnfoldedHeatFluxCalculator(Model(), virials_reference=atoms)

            calc.calculate(atoms)

    def test_consistency(self):
        from ase.io import read
        from gknet.experimental.fast_calculator import fastCalculator

        atoms = read("assets/zro_mono_primitive.in") * [2, 2, 2]
        atoms.rattle()
        atoms.set_velocities(np.random.random((len(atoms), 3)))

        og = fastCalculator("assets/model_n1.torch", heat_flux=True, virials=True, hardy=True, skin=0)
        uf = UnfoldedHeatFluxCalculator("assets/model_n1.torch", skin=0, skin_unfolder=0)

        og_hf = og.calculate(atoms)["heat_flux"]
        uf_hf = uf.calculate(atoms)["heat_flux"]

        np.testing.assert_allclose(og_hf, uf_hf, atol=5e-5)
