import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from tbx.load import ensemble
from tbx import gk, basedir, get_and_concatenate

from pathlib import Path

basedir = Path(
    "/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1"
)


def get_folder(phase, temp, n):
    if phase == "m":
        return monoclinic_folder(temp, n)
    else:
        return tetragonal_folder(temp, n)


def tetragonal_folder(temp, n):
    if temp in [1400]:
        return basedir / f"variations_tex_2/{temp}/n_{n}"
    else:
        raise KeyError(f"{temp} not available for phase tetragonal")


def monoclinic_folder(temp, n):
    if temp in [300, 600, 1400]:
        return basedir / f"variations_mex_2/{temp}/n_{n}"
    else:
        raise KeyError(f"{temp} not available for phase monoclinic")


def filename(maxsteps, spacing=2, freq=1.0):
    if spacing == 1:
        return f"gk_unfolded_r0.to_{maxsteps}.freq_{freq:.2f}.nc"
    else:
        return f"gk_unfolded_r0.to_{maxsteps}.every_{spacing}.freq_{freq:.2f}.nc"


def get_dataset(phase, temp, n, maxsteps):
    return gk.combine(
        ensemble(
            get_folder(phase, temp, n),
            "recompute/maxsteps_unfolded_r0",
            filename(maxsteps, spacing=2, freq=1.0),
        )
    )


def get_kappa(phase, temp, n, maxsteps):
    data = get_dataset(phase, temp, n, maxsteps)
    return gk.get_kappa(data, a=None, eps=0)


thermos = [("m", 300), ("m", 600), ("m", 1400), ("t", 1400)]
n_atomss = [96, 324, 768, 1500, 2592, 4116]
maxstepss = range(25000, 500001, 25000)

for phase, temp in thermos:
    outfile = Path(f"{phase}_{temp}.nc")
    if outfile.is_file():
        print(f"{outfile} exists, skip")
        continue

    print(f"working on {outfile.stem}")

    def get_maxsteps(n, maxsteps):
        k, e = get_kappa(phase, temp, n, maxsteps)
        k = xr.DataArray(k, name="kappa_mean")
        e = xr.DataArray(e, name="kappa_stderr")

        d = xr.Dataset({"kappa_mean": k, "kappa_stderr": e})

        return d

    def get_maxstepss(n):
        return get_and_concatenate(
            lambda maxsteps: get_maxsteps(n, maxsteps), maxstepss, "maxsteps"
        )

    def get_n_atomss():
        return get_and_concatenate(lambda n: get_maxstepss(n), n_atomss, "n_atoms")

    data = get_n_atomss()
    data.to_netcdf(outfile)

