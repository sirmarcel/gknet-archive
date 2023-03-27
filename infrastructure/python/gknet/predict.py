import numpy as np

from pathlib import Path

from vibes.context import TaskContext

from .train.trainer import get_loader
from .helpers import guess_device_settings, talk
from gknet import keys


def predict(
    model, loader, outfile=None, device=None, parallel=None, stress=False
):
    from gknet import load

    model = load(model)

    device, parallel = guess_device_settings(device=device, parallel=parallel)
    model.parallel = parallel
    model.stress = stress
    properties = [keys.energy, keys.forces]
    if stress:
        properties.append(keys.stress)

    model.model.to(device)

    predictions = {prop: [] for prop in properties}
    true = {prop: [] for prop in properties}
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        result = model.model(batch)

        for prop in properties:
            predictions[prop].append(result[prop].cpu().detach().numpy())
            true[prop].append(batch[prop].cpu().detach().numpy())

    data = {}
    for prop in properties:
        data[f"pred_{prop}"] = np.concatenate(predictions[prop])
        data[f"true_{prop}"] = np.concatenate(true[prop])

    if outfile is not None:
        np.savez_compressed(outfile, **data)
    else:
        return data


default = {
    "predict": {
        "device": None,
        "parallel": None,
        "stress": False,
        "batch_size": 50,
        "datasets": [],
        "model": Path(".") / "train/best_model.torch",
    }
}


class PredictContext(TaskContext):
    def __init__(self, settings=None, workdir=Path("predict")):
        if settings is None:
            settings = {}

        super().__init__(
            settings, "predict", workdir=workdir, template_dict=default
        )

    def run(self):
        device, parallel = guess_device_settings(
            self.kw.device, self.kw.parallel
        )

        self.workdir.mkdir(exist_ok=True)

        from gknet import load

        model = load(self.kw.model)

        talk(f"Loaded model, saving to {self.workdir}/model.torch.")
        model.save(self.workdir / "model")

        for data in self.kw.datasets:
            talk(f"Predicting for {data}...")
            loader = get_loader(
                data, batch_size=self.kw.batch_size, shuffle=False
            )
            outfile = self.workdir / f"{Path(data).stem}.npz"
            predict(
                model,
                loader,
                outfile=outfile,
                device=device,
                parallel=parallel,
                stress=self.kw.stress,
            )
            talk("Done, saved results.")

        return True
