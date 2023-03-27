import torch
from cmlkit.engine import Configurable

from gknet import keys
from gknet.helpers import stress_to_voigt


def mse(true, pred, weight):
    diff = true - pred
    if hasattr(torch, "nan_to_num"):
        # this will ensure that missing stress is not counted
        diff = torch.nan_to_num(diff)

    diff = diff**2
    diff = torch.mean(diff, dim=0)
    diff *= weight  # doing it here means we can apply weights to each entry
    return torch.mean(diff)


class MSE(Configurable):

    kind = "mse"

    def __init__(self, energy=0.001, forces=0.999, stress=None):
        self.energy, self.config_energy = get_weight(energy)
        self.forces, self.config_forces = get_weight(forces)
        self.stress, self.config_stress = get_weight(stress)

    def _get_config(self):
        return {
            "energy": self.config_energy,
            "forces": self.config_forces,
            "stress": self.config_stress,
        }

    def __call__(self, true, pred):
        loss = 0.0

        if self.energy is not None:
            loss += mse(true[keys.energy], pred[keys.energy], weight=self.energy)

        if self.forces is not None:
            loss += mse(true[keys.forces], pred[keys.forces], weight=self.forces)

        if self.stress is not None:
            loss += mse(true[keys.stress], pred[keys.stress], weight=self.stress)

        return loss

    def to(self, device="cpu"):
        if isinstance(self.forces, torch.Tensor):
            self.forces = self.forces.to(device)

        if isinstance(self.stress, torch.Tensor):
            self.stress = self.stress.to(device)


def get_weight(weight):
    if weight is None:
        return None, None
    elif isinstance(weight, float):
        return weight, weight
    elif isinstance(weight, list):
        return torch.tensor(weight), weight
    else:
        raise ValueError(f"Don't know how to treat weight {weight}.")


class SMSE(Configurable):
    """Scaled MSE

    MSE that's scaled by the variance. This is the term that
    appears in the coefficient of determiniation, so R2 = 1-SMSE.

    We also symmetrise the stress to avoid redundant terms.
    """

    kind = "smse"

    def __init__(
        self,
        energy=0.001,
        forces=0.999,
        stress=None,
        var_energy=1.0,
        var_forces=[1.0] * 3,
        var_stress=[1.0] * 6,
    ):
        self.energy, self._energy = convert_and_keep(energy)
        self.forces, self._forces = convert_and_keep(forces)
        self.stress, self._stress = convert_and_keep(stress)

        self.var_energy, self._var_energy = convert_and_keep(var_energy)
        self.var_forces, self._var_forces = convert_and_keep(var_forces)
        self.var_stress, self._var_stress = convert_and_keep(var_stress)

    def _get_config(self):
        return {
            "energy": self.energy,
            "forces": self.forces,
            "stress": self.stress,
            "var_energy": self.var_energy,
            "var_forces": self.var_forces,
            "var_stress": self.var_stress,
        }

    def __call__(self, true, pred):
        loss = 0.0

        loss += scaled_mse(
            true[keys.energy],
            pred[keys.energy],
            weight=self._energy,
            variance=self._var_energy,
        )

        loss += scaled_mse(
            true[keys.forces],
            pred[keys.forces],
            weight=self._forces,
            variance=self._var_forces,
            dim_mean=1,  # need to average over atoms first
        )

        if self.stress is not None:
            loss += scaled_mse(
                stress_to_voigt(true[keys.stress]),
                stress_to_voigt(pred[keys.stress]),
                variance=self._var_stress,
                weight=self._stress,
            )

        return loss

    def to(self, device="cpu"):
        self._energy = self._energy.to(device)
        self._forces = self._forces.to(device)
        self._var_energy = self._var_energy.to(device)
        self._var_forces = self._var_forces.to(device)
        self._var_stress = self._var_stress.to(device)

        if self._stress is not None:
            self._stress = self._stress.to(device)


def convert_and_keep(item):
    if item is not None:
        return item, torch.tensor(item)
    else:
        return None, None


def scaled_mse(true, pred, variance, weight, dim_mean=None):
    diff = true - pred
    if hasattr(torch, "nan_to_num"):
        # this will ensure that missing stress is not counted
        diff = torch.nan_to_num(diff)

    diff = diff**2
    if dim_mean is not None:
        diff = diff.mean(dim_mean)

    diff /= variance.unsqueeze(0)
    return torch.mean(diff) * weight
