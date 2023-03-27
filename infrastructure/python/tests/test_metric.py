import torch
import numpy as np
from unittest import TestCase
from ase.io import Trajectory
import schnetpack as spk

from gknet import keys
from gknet.data import Data


from gknet.train.metric import ScaledMSE
from gknet.loss import stress_to_voigt


class TestScaledMSE(TestCase):
    def test_basic(self):
        data = Data()
        data.add_atoms(iterable=Trajectory("md.traj"), stress=True)
        energy = data.energy
        forces = torch.concat(data.forces)
        stress = data.stress

        loader = spk.AtomsLoader(data, shuffle=True, batch_size=2)

        energy_metric = ScaledMSE.from_data(keys.energy, data)
        forces_metric = ScaledMSE.from_data(keys.forces, data)
        stress_metric = ScaledMSE.from_data(keys.stress, data)

        for batch in loader:
            energy_metric.add_batch(batch, {keys.energy: energy.mean(0).unsqueeze(0)})
            forces_metric.add_batch(
                batch, {keys.forces: forces.mean((0, 1)).unsqueeze(0)}
            )
            stress_metric.add_batch(batch, {keys.stress: stress.mean(0).unsqueeze(0)})

        for metric in [energy_metric, forces_metric, stress_metric]:
            result = metric.aggregate()
            np.testing.assert_allclose(result, 1.0, atol=1e-7)

        loader = spk.AtomsLoader(data, shuffle=True, batch_size=2)
        for metric in [energy_metric, forces_metric, stress_metric]:
            metric.reset()

        for batch in loader:
            energy_metric.add_batch(
                batch, {keys.energy: 1.1 * energy.mean(0).unsqueeze(0)}
            )
            forces_metric.add_batch(
                batch,
                {
                    keys.forces: 0.5 + forces.mean((0, 1)).unsqueeze(0)
                },  # force mean is zero
            )
            stress_metric.add_batch(
                batch, {keys.stress: 1.1 * stress.mean(0).unsqueeze(0)}
            )

        for metric in [energy_metric, forces_metric, stress_metric]:
            result = metric.aggregate()
            print(result)
            np.testing.assert_array_less(1.0, result)
