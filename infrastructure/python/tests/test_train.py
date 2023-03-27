import torch
from unittest import TestCase
from ase.io import Trajectory


from tempdir import Tempdir


class TestTrainer(Tempdir, TestCase):
    def test_roundtrip(self):
        for schedulers in [
            [{"decay_lr_on_plateau": {}}, {"stop_on_plateau": {}}],
            [{"plateau": {}}, {"early_stopping": {}}],
        ]:
            for scaled_metrics in [True, False]:
                for loss in [{"mse": {"stress": 10.0}}, {"smse": {"stress": 10.0}}]:
                    import gknet

                    self.reset_tempdir()

                    data = gknet.Data()
                    data.add_file("md.traj")
                    data.save(self.tempdir / "data")

                    factory = gknet.train.Trainer(
                        train={
                            "data": self.tempdir / "data.torch",
                            "batch_size": 2,
                            "shuffle": True,
                        },
                        validate={
                            "data": self.tempdir / "data.torch",
                            "batch_size": 2,
                            "shuffle": False,
                        },
                        loss=loss,
                        schedulers=schedulers,
                        optimizer={"adam": {}},
                        scaled_metrics=scaled_metrics,
                    )

                    model = {"model": {}}

                    trainer = factory.prepare(model, directory=self.tempdir / "train")
                    trainer.train(device="cpu", n_epochs=2)

                    # just testing that nothing explodes

                    trainer2 = factory.prepare(model, directory=self.tempdir / "train")
