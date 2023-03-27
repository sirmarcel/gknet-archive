import torch
from gknet import keys

from gknet.helpers import stress_to_voigt


class ScaledMSE:
    def __init__(self, prop, variance):
        self.prop = prop

        if isinstance(variance, torch.Tensor):
            self.variance = variance
        else:
            self.variance = torch.tensor(variance)

        self.name = f"SMSE_{self.prop}"

        self.reset()

    @classmethod
    def from_data(cls, prop, data):
        if prop == keys.energy:
            return cls(prop, data.var_energy)
        elif prop == keys.forces:
            return cls(prop, data.var_forces)
        elif prop == keys.stress:
            return cls(prop, data.var_stress_voigt)
        else:
            raise ValueError(f"cannot deal with property {prop}")

    def add_batch(self, batch, result):
        diffs_over_batch = compute(batch, result, self.prop)
        self.count += diffs_over_batch.shape[0]

        diffs_over_batch = diffs_over_batch.detach().cpu()

        if self.prop == keys.forces:
            diffs_over_batch = diffs_over_batch.mean(1)  # mean over atoms

        diffs_scaled = diffs_over_batch / self.variance.unsqueeze(0)
        self.result += float(diffs_scaled.mean(1).sum(0))

    def aggregate(self):
        return self.result / self.count

    def reset(self):
        self.result = 0.0
        self.count = 0


def compute(true, pred, key):
    if key == keys.stress:
        true = stress_to_voigt(true[key])
        pred = stress_to_voigt(pred[key])
    else:
        true = true[key]
        pred = pred[key]

    return (true - pred) ** 2
