from pathlib import Path

import schnetpack as spk
from cmlkit.engine import Configurable
from vibes.helpers import warn

from gknet.engine import Stateful, read_yaml, save_yaml
from gknet.helpers import talk

from gknet import keys


class Trainer(Configurable):
    kind = "trainer"

    def __init__(
        self,
        train,
        validate,
        loss={"mse": {}},
        schedulers=[{"plateau": {}}, {"early_stopping": {}}],
        optimizer={"adam": {}},
        scaled_metrics=False,
    ):
        self.config_loader_train = get_loader_config(**train)
        self.config_loader_validate = get_loader_config(**validate)

        from gknet import from_config

        self.loss = from_config(loss)

        self.schedulers = [from_config(scheduler) for scheduler in schedulers]

        self.needs_stress = self.loss.stress is not None

        self.optimizer = from_config(optimizer)

        targets = [(keys.energy, False), (keys.forces, True)]
        if self.needs_stress:
            targets.append((keys.stress, True))

        self.scaled_metrics = scaled_metrics
        if not self.scaled_metrics:
            self.metrics = []
            for target, element_wise in targets:
                self.metrics.append(
                    spk.train.metrics.MeanAbsoluteError(
                        target=target, element_wise=element_wise
                    )
                )
        else:
            self.metrics = get_scaled_metrics(self.config_loader_validate["data"], targets)

    def _get_config(self):
        return {
            "train": self.config_loader_train,
            "validate": self.config_loader_validate,
            "loss": self.loss.get_config(),
            "schedulers": [s.get_config() for s in self.schedulers],
            "optimizer": self.optimizer.get_config(),
            "scaled_metrics": self.scaled_metrics,
        }

    def prepare(self, model, directory="train", device="cpu", parallel=False):
        directory = Path(directory)

        from gknet import from_config

        model = from_config(model)
        model.parallel = parallel

        self.loss.to(device)

        if directory.exists():
            talk("Trainer directory already exists, will restore.")
            if not read_yaml(directory / "trainer.yaml") == self.get_config():
                warn(
                    f"Mismatched Trainer settings during restore, proceed with caution!",
                    level=1,
                )
            if not read_yaml(directory / "model.yaml") == model.get_config():
                warn(
                    f"Mismatched Model settings during restore, proceed with caution!",
                    level=1,
                )
                print(model.get_config())
                print(read_yaml(directory / "model.yaml"))
        else:
            talk("Trainer directory does not exist, backing up settings!")
            directory.mkdir()
            save_yaml(directory / "trainer.yaml", self.get_config())
            save_yaml(directory / "model.yaml", model.get_config())

        model.stress = self.needs_stress
        spk_model = model.model

        optimizer = self.optimizer.prepare(spk_model)

        hooks = [scheduler.prepare(optimizer) for scheduler in self.schedulers]
        hooks.append(spk.train.hooks.CSVHook(directory, self.metrics))

        loader_train = get_loader(**self.config_loader_train)
        loader_validate = get_loader(**self.config_loader_validate)

        return spk.train.trainer.Trainer(
            model_path=directory,
            model=spk_model,
            loss_fn=self.loss,
            optimizer=optimizer,
            train_loader=loader_train,
            validation_loader=loader_validate,
            keep_n_checkpoints=3,
            checkpoint_interval=10,
            validation_interval=1,
            hooks=hooks,
            loss_is_normalized=True,
        )


def get_loader_config(data, batch_size=64, shuffle=True):
    return {"data": str(data), "batch_size": batch_size, "shuffle": shuffle}


def get_loader(data, batch_size=64, shuffle=True):
    from gknet import load

    loaded = load(data)
    return spk.AtomsLoader(loaded, shuffle=shuffle, batch_size=batch_size)


def get_scaled_metrics(valid, targets):
    from gknet import load
    from .metric import ScaledMSE

    data = load(valid)

    metrics = []
    for target, _ in targets:
        metrics.append(ScaledMSE.from_data(target, data))

    return metrics
