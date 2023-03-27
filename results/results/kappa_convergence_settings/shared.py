import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from tbx.load import ensemble
from tbx import gk, basedir

from pathlib import Path

basedir = Path(
    "/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1"
)

# coordinates of interest
convergence_coords = {
    "unconverged": [96, 25000],
    "unconverged_long": [96, 250000],
    "semi": [768, 125000],
    "converged": [1500, 250000],
    "converged_short": [1500, 25000],
    "ultra": [4116, 500000],
}

default_freq = 1.00


def get_folder(phase, temp, n):
    if phase == "m":
        return monoclinic_folder(temp, n)
    else:
        return tetragonal_folder(temp, n)


def tetragonal_folder(temp, n):
    if temp in [1400]:
        return basedir / f"variations_tex_2/{temp}/n_{n}"
    else:
        return basedir / f"tetragonal_exp_real_prod_1/{temp}/n_{n}"


def monoclinic_folder(temp, n):
    if temp in [300, 600, 1400]:
        return basedir / f"variations_mex_2/{temp}/n_{n}"
    else:
        return basedir / f"monoclinic_exp_real_prod_1/{temp}/n_{n}"


def filename(hf="unfolded_r0", total=False, spacing=1, freq=1.00, maxsteps=250000):
    if not total:
        total = ""
    else:
        total = ".total"

    if spacing == 1:
        spacing = ""
    else:
        spacing = f".every_{spacing}"

    freq = f".freq_{freq:.2f}"
    maxsteps = f".to_{maxsteps}"

    return f"gk_{hf}{total}{maxsteps}{spacing}{freq}.nc"


def get_ens(temp=300, n=1500, phase="m", **hfargs):
    folder = get_folder(phase, temp, n)

    file = filename(**hfargs)

    return ensemble(folder, "recompute", file)


def get_mean(**kwargs):
    return gk.combine(get_ens(**kwargs))


def get_and_concatenate(getter, quantity, name):
    data = [getter(q) for q in quantity]
    data = xr.concat(data, dim=xr.DataArray(data=quantity, name=name, dims=(name)))

    return data
