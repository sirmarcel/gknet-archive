import numpy as np
import xarray as xr

from vibes import keys


def get_mean_kappa(datasets):

    # concatentate trajectories
    ds_gk = xr.concat(datasets, dim=keys.trajectory)
    attrs = {ii: d.attrs for (ii, d) in enumerate(datasets)}
    ds_gk.attrs = attrs

    ks = np.array([np.diag(k) for k in ds_gk.kappa]).flatten()
    k_mean = ks.mean()
    k_err = (ks.var() / (len(ks))) ** 0.5

    return k_mean, k_err
