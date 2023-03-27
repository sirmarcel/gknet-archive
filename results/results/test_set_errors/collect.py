import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from pathlib import Path
from tbx import load_data


datasets = ["nomad"]
cutoffs = [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
ts = [1, 2, 3, 5]

properties = ["forces"]
transforms = {"forces": lambda x: np.mean(np.abs(x), axis=(1, 2))}


def get_errors(folder, dataset, prop):
    raw_data = load_data(folder / f"predict/{dataset}.npz")

    transform = transforms[prop]
    diff = raw_data[f"true_{prop}"] - raw_data[f"pred_{prop}"]

    return transform(diff)


def name(cu, t):
    return f"{cu:.1f}_{t}"


def get_folder(cu, t):
    return basedir / (f"cu_{cu:.1f}_e_inpt_4387/train_n{t}_s1/")


basedir = Path("/u/mlang/gknet/gknet/experiments/ccl_zro_t96/")

for dataset in datasets:
    data = {}
    for p in properties:
        raw_data = [
            [get_errors(get_folder(cu, t), dataset, p) for cu in cutoffs] for t in ts
        ]
        raw_data = np.array(raw_data)

        data[p] = xr.DataArray(
            data=raw_data,
            dims=("t", "cutoff", "sample"),
            coords={"cutoff": np.array(cutoffs), "t": np.array(ts)},
            name=p,
        )

    data_set = xr.Dataset(data_vars=data, coords={"property": properties})

    data_set.to_netcdf(f"{dataset}.nc")
