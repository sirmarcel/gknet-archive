import torch
from cmlkit.engine import Configurable
from cmlkit.engine.inout import normalize_extension


def load(path):

    if isinstance(path, Stateful):
        return path
    else:
        path = normalize_extension(path, ".torch")

        payload = torch.load(path)

        config = payload["config"]
        state = payload["state"]

        from gknet import from_config

        obj = from_config(config)
        obj.restore(state)

        return obj


class Stateful(Configurable):
    def get_dict(self):
        config = self.get_config()
        state = self.get_state()

        return {"config": config, "state": state}

    def save(self, path):
        path = normalize_extension(path, ".torch")

        torch.save(self.get_dict(), path)

    def restore(self, state):
        return self._restore(state)

    def get_state(self):
        return self._get_state()
