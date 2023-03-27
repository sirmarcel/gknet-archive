import numpy as np
import xarray as xr
from pathlib import Path

from .green_kubo import get_mean_kappa


class Kurve:
    """Data container for kappa vs temperature with errors.

    Mostly exists to define a canonical format, and to simplify
    reading out results, at least somewhat.

    The idea is simple: We store a dict internally, which makes it
    easy to add things out of order, but only emit sorted numpy arrays.

    This is horrendously inefficient, but since we probably won't get
    above, like, 10 entries, it doesn't seem useful to bother with
    optimisation. If we wanted to, we could cache the sorting operations,
    or put some efforts into just doing out-of-order insertions in numpy
    arrays efficiently.

    """

    def __init__(self, name, description="", label=None):
        self.name = name
        self.description = description  # internal description
        if label is None:
            self.label = name
        else:
            self.label = label  # for plotting

        self._data = {}

    @property
    def data(self):
        return dict(sorted(self._data.items()))

    @property
    def temperatures(self):
        return np.array(list(self.data.keys()), dtype=float)

    @property
    def kappas(self):
        return np.array([v[0] for v in self.data.values()], dtype=float)

    @property
    def errors(self):
        return np.array([v[1] for v in self.data.values()], dtype=float)

    def add(self, temperature, kappa, error):
        self._data[temperature] = (float(kappa), float(error))

    def add_arrays(self, temperatures, kappas, errors):
        for i, t in enumerate(temperatures):
            self.add(t, kappas[i], errors[i])

    def add_datasets(self, temperature, datasets):
        kappa, error = get_mean_kappa(datasets)

        self.add(temperature, kappa, error)

    def add_folder_ensemble(
        self, temperature, folder, ensemble, datafile="md/greenkubo.nc"
    ):
        base = Path(folder)
        files = [base / Path(e) / datafile for e in ensemble]
        if base.is_dir():
            datasets = []
            for file in files:
                if file.is_file():
                    datasets.append(xr.open_dataset(file))

            if len(datasets) > 0:
                self.add_datasets(temperature, datasets)
                return True

        print(f"Did not find data in {base}, what's up with that?")
