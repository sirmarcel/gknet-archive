import torch
import schnetpack as spk

from cmlkit.engine import Configurable


class Adam(Configurable):

    kind = "adam"

    def __init__(self, lr=1e-3):
        self.lr = lr

    def _get_config(self):
        return {"lr": self.lr}

    def prepare(self, model):
        return torch.optim.Adam(params=model.parameters(), lr=self.lr)
