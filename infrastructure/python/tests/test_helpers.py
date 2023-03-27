from unittest import TestCase
import torch
import numpy as np

from gknet.helpers import stress_to_voigt


class TestHelpers(TestCase):
    def test_stress_helper(self):
        import numpy as np
        from ase.constraints import full_3x3_to_voigt_6_stress

        stress = torch.rand(10, 3, 3)
        stress = 0.5 * (stress + stress.transpose(1, 2))

        a = stress_to_voigt(stress).numpy()
        b = full_3x3_to_voigt_6_stress(stress.numpy())

        np.testing.assert_allclose(a, b)
