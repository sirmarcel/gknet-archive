import schnetpack as spk

from cmlkit.engine import Configurable


class Plateau(Configurable):
    kind = "plateau"

    def __init__(
        self,
        patience=20,
        factor=0.5,
        min_lr=1.0e-6,
        window_length=1,
        stop_after_min=False,
    ):
        self.patience = patience
        self.factor = factor
        self.min_lr = min_lr
        self.window_length = window_length
        self.stop_after_min = stop_after_min

    def _get_config(self):
        return {
            "patience": self.patience,
            "factor": self.factor,
            "min_lr": self.min_lr,
            "window_length": self.window_length,
            "stop_after_min": self.stop_after_min,
        }

    def prepare(self, optimizer):
        return spk.train.ReduceLROnPlateauHook(
            optimizer,
            patience=self.patience,
            factor=self.factor,
            min_lr=self.min_lr,
            window_length=self.window_length,
            stop_after_min=self.stop_after_min,
        )


class EarlyStopping(Configurable):

    kind = "early_stopping"

    def __init__(self, patience=25):
        self.patience = patience

    def _get_config(self):
        return {"patience": self.patience}

    def prepare(self, optimizer):
        return spk.train.EarlyStoppingHook(patience=self.patience)
