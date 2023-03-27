import torch
from pathlib import Path

from vibes.context import TaskContext
from vibes.helpers.watchdogs import SlurmWatchdog
from vibes.helpers.restarts import restart
from vibes.helpers import warn

from gknet.engine import read_yaml
from gknet.helpers import talk, guess_device_settings

default = {
    "train": {
        "model": "model.yaml",
        "trainer": "trainer.yaml",
        "steps_per_loop": 20,
        "parallel": None,
        "device": None,
        "warm_start": None,
    }
}


class TrainContext(TaskContext):
    def __init__(self, settings=None, workdir=Path("train")):
        if settings is None:
            settings = {}

        super().__init__(settings, "train", workdir=workdir, template_dict=default)

        from gknet import from_config

        self.factory = from_config(read_yaml(self.kw.trainer))

        self.model_config = read_yaml(self.kw.model)
        self.warm_start = self.kw.warm_start
        if self.warm_start is not None:
            from gknet import load

            model = load(self.warm_start)
            if not model.get_config() == self.model_config:
                warn(
                    "warm start model is mismatched with model config, things may break"
                )

    def _run(self):
        from gknet import load
        from gknet import from_config

        device, parallel = guess_device_settings(self.kw.device, self.kw.parallel)

        if self.warm_start:
            model = load(self.warm_start)
            # SchNetPack trainer will overwrite weights with checkpoint
            # upon restart -- so we don't need to worry!
        else:
            model = from_config(self.model_config)

        trainer = self.factory.prepare(
            model, directory=self.workdir, device=device, parallel=parallel
        )

        watchdog = SlurmWatchdog(log=self.workdir / "watchdog.log", verbose=False)

        talk("Training...")
        while not watchdog() and not trainer._stop:
            trainer.train(n_epochs=self.kw.steps_per_loop, device=device)
            self.log_state(trainer)

        if trainer._stop:
            talk("Trainer is done.")

            model = from_config(self.model_config)
            best = torch.load(trainer.best_model)
            if parallel:
                best_state = best.module.state_dict()
            else:
                best_state = best.state_dict()
            model._restore(best_state)
            model.save(self.workdir / "best_model.torch")

            return True
        else:
            talk("Trainer isn't done, but stopped due to timeout. Saving checkpoint.")
            trainer.store_checkpoint()

            return False

    def run(self):
        done = self._run()

        if not done:
            restart(self.settings)

    def log_state(self, trainer):
        msg = f"... epoch {trainer.epoch}."
        for i, scheduler in enumerate(self.factory.schedulers):
            if scheduler.kind in [
                "early_stopping",
                "decay_lr_on_plateau",
                "stop_on_plateau",
            ]:
                msg += f" {scheduler.kind}: {trainer.hooks[i].counter}, {trainer.hooks[i].best_loss:.16e}."

            if scheduler.kind == "plateau":
                msg += f" {scheduler.kind}: {trainer.hooks[i].scheduler.num_bad_epochs}, {trainer.hooks[i].scheduler.best:.16e}."

        talk(msg)
