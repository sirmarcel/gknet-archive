from unittest import TestCase
import torch
import numpy as np

from gknet.loss import MSE, SMSE, stress_to_voigt
from gknet import keys


class TestMSE(TestCase):
    def setUp(self):
        self.true = {
            keys.energy: torch.tensor([1.0, 1.0]),
            keys.forces: torch.tensor([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]]),
        }
        self.pred = {
            keys.energy: torch.tensor([2.0, 2.0]),
            keys.forces: torch.tensor([[1.0, 7.0, 1.0], [8.0, 2.0, 2.0]]),
        }

    def test_basic(self):
        loss = MSE(energy=0.5, forces=None, stress=None)
        self.assertEqual(loss(self.true, self.pred), 0.5 * 1.0)

        loss = MSE(energy=None, forces=0.5, stress=None)
        self.assertEqual(loss(self.true, self.pred), 0.5 * 72.0 / 6.0)

        loss = MSE(energy=None, forces=[0.5, 1.0, 0.0], stress=None)
        self.assertEqual(loss(self.true, self.pred), (18.0 / 2 + 18.0) / 3.0)


class TestSMSE(TestCase):
    def setUp(self):
        self.true = {
            keys.energy: torch.rand(10, 1),
            keys.forces: torch.rand(10, 25, 3),
            keys.stress: torch.rand(10, 3, 3),
        }
        self.true["var_energy"] = torch.var(self.true[keys.energy], 0, unbiased=False)
        self.true["var_forces"] = torch.var(self.true[keys.forces], (0, 1), unbiased=False)
        self.true["var_stress"] = torch.var(
            stress_to_voigt(self.true[keys.stress]), 0, unbiased=False
        )

        self.pred_mean = {}
        self.pred_mean[keys.energy] = torch.mean(self.true[keys.energy], 0).unsqueeze(0)
        self.pred_mean[keys.forces] = torch.mean(self.true[keys.forces], (0, 1)).unsqueeze(0)
        self.pred_mean[keys.stress] = torch.mean(self.true[keys.stress], 0).unsqueeze(0)

        # shouldn't use a multiplier to break stuff -- force mean is ~zero!
        # (of course here we have random numbers)
        self.pred_off = {k: v + 1.0 for k, v in self.pred_mean.items()}

    def test_basic(self):
        for a, b, c in [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1 / 2, 1 / 2, 0],
            [1 / 2, 1 / 2, None],
            [1 / 3, 1 / 3, 1 / 3],
        ]:
            print(f"{a},{b},{c}")

            loss = SMSE(
                energy=a,
                forces=b,
                stress=c,
                var_energy=self.true["var_energy"],
                var_forces=self.true["var_forces"],
                var_stress=self.true["var_stress"],
            )
            np.testing.assert_allclose(loss(self.true, self.pred_mean), 1.0, atol=1e-7)
            self.assertGreater(loss(self.true, self.pred_off), 1.0)

    def test_stress_helper(self):
        import numpy as np
        from ase.constraints import full_3x3_to_voigt_6_stress

        stress = torch.rand(10, 3, 3)
        stress = 0.5 * (stress + stress.transpose(1, 2))

        a = stress_to_voigt(stress).numpy()
        b = full_3x3_to_voigt_6_stress(stress.numpy())

        np.testing.assert_allclose(a, b)
