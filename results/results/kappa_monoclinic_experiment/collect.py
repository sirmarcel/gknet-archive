import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from tbx import gk, load, basedir

prod_folder = basedir / "cu_5.0_e_inpt_4387/train_n2_s1/monoclinic_exp_real_prod_1/"
test_folder_mex_2 = basedir / "cu_5.0_e_inpt_4387/train_n2_s1/variations_mex_2/"

a = None
eps = 0
test_temps_mex_2 = [300, 600, 1400]
prod_temps = [350, 400, 450, 750, 900, 1050, 1200]
all_temps = list(sorted(test_temps_mex_2 + prod_temps))

# settings
freq = 1.00
maxsteps = 250000
spacing = 2
n_atoms = 1500


def get_prod_dataset(temp, freq=3.00):
    return gk.combine(
        load.ensemble(
            prod_folder / f"{temp}/n_{n_atoms}",
            "recompute",
            f"gk_unfolded_r0.every_{spacing}.to_{int(maxsteps/spacing)}.freq_{freq:.2f}.nc",
        )
    )


def get_test_dataset_mex_2(temp, freq=3.00):
    return gk.combine(
        load.ensemble(
            test_folder_mex_2 / f"{temp}/n_{n_atoms}",
            "recompute/maxsteps_unfolded_r0/",
            f"gk_unfolded_r0.to_{maxsteps}.every_{spacing}.freq_{freq:.2f}.nc",
        )
    )


def get_data(freq):
    data = np.zeros((len(all_temps), 2))

    for i, temp in enumerate(all_temps):
        print(f"collecting temp={temp}")
        if temp in test_temps_mex_2:
            data[i] = gk.get_kappa(
                get_test_dataset_mex_2(temp, freq=freq), a=a, eps=eps
            )
        else:
            data[i] = gk.get_kappa(get_prod_dataset(temp, freq=freq), a=a, eps=eps)

    return data


def make_dataset(freq):
    data = get_data(freq)

    coords = {"temperature": np.array(all_temps)}
    kappa_mean = xr.DataArray(
        data=data[:, 0],
        dims=("temperature"),
        coords=coords,
        name="kappa_mean",
    )
    kappa_stderr = xr.DataArray(
        data=data[:, 1],
        dims=("temperature"),
        coords=coords,
        name="kappa_stderr",
    )

    return xr.Dataset({"kappa_mean": kappa_mean, "kappa_stderr": kappa_stderr})


data = make_dataset(freq)

data.to_netcdf(f"result_cu5_n2.nc")
