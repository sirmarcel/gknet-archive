from pathlib import Path

from vibes.context import TaskContext
from vibes.helpers.watchdogs import SlurmWatchdog
from vibes.helpers.restarts import restart

from .workflow import Recompute


default = {
    "recompute": {
        "infolder": Path("md/trajectory/"),
        "outfolder": "data",
        "batch_size": 1000,
        "batched": False,
        "step": 1,
        "stop": None,
    }
}


class RecomputeContext(TaskContext):
    def __init__(self, settings=None, workdir=Path("recompute")):
        if settings is None:
            settings = {}

        super().__init__(settings, "recompute", workdir=workdir, template_dict=default)

    def run(self):
        watchdog = SlurmWatchdog(log=self.workdir / "watchdog.log", verbose=False)

        recompute = Recompute(
            self.kw.infolder,
            self.workdir / self.kw.outfolder,
            self.calculator,
            batch_size=self.kw.batch_size,
            batched=self.kw.batched,
            step=self.kw.step,
            stop=self.kw.stop,
        )

        done = recompute.run(watchdog)

        if not done:
            restart(self.settings)
