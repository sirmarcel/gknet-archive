from cmlkit.engine import Configurable
from schnetpack.train.hooks.base_hook import Hook  # for on_* methods

class Plateau(Hook):
    def __init__(self, patience=25, tolerance=1e-4):
        self.patience = patience
        self.tolerance = tolerance

        self.best_loss = float("Inf")
        self.counter = 0

    def triggered(self, loss):
        if loss > (1 - self.tolerance) * self.best_loss:
            self.counter += 1

        else:
            self.best_loss = loss
            self.counter = 0

        return self.counter > self.patience

    @property
    def state_dict(self):
        return {"counter": self.counter, "best_loss": self.best_loss}

    @state_dict.setter
    def state_dict(self, state_dict):
        self.counter = state_dict["counter"]
        self.best_loss = state_dict["best_loss"]


class StopOnPlateau(Plateau, Configurable):
    """Early stopping"""

    kind = "stop_on_plateau"

    def __init__(self, patience=25, tolerance=1e-4):
        super().__init__(patience=patience, tolerance=tolerance)

    def _get_config(self):
        return {"patience": self.patience, "tolerance": self.tolerance}

    def prepare(self, optimizer):
        return self

    def on_validation_end(self, trainer, loss):
        if self.triggered(loss):
            trainer._stop = True


class DecayLROnPlateau(Plateau, Configurable):
    """LR decay on plateau"""

    kind = "decay_lr_on_plateau"

    def __init__(
        self,
        patience=20,
        tolerance=1e-4,
        factor=0.5,
        min_lr=1.0e-6,
        stop_after_min=False,
    ):
        super().__init__(patience=patience, tolerance=tolerance)

        self.factor = factor
        self.min_lr = min_lr
        self.stop_after_min = stop_after_min

        self.optimizer = None
        self.best_loss = float("Inf")
        self.counter = 0

    def _get_config(self):
        return {
            "patience": self.patience,
            "tolerance": self.tolerance,
            "factor": self.factor,
            "min_lr": self.min_lr,
            "stop_after_min": self.stop_after_min,
        }

    def prepare(self, optimizer):
        self.optimizer = optimizer

        return self

    def on_validation_end(self, trainer, loss):
        if self.triggered(loss):
            reached_min = self.decrease()
            if self.stop_after_min and reached_min:
                trainer._stop = True

    def decrease(self):
        reached_min = False

        for i, param_group in enumerate(self.optimizer.param_groups):
            old_lr = float(param_group["lr"])
            new_lr = max(old_lr * self.factor, self.min_lr)
            param_group["lr"] = new_lr

            if new_lr == self.min_lr:
                reached_min = True

        return reached_min
