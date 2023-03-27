from pathlib import Path
import numpy as np
import xarray as xr
import yaml

tasks = {
    Path("/u/mlang/gknet/gknet/experiments/oneoff/heat_flux_timings/"): "zro_schnet_n2.nc",
    Path("/u/mlang/gknet/gknet/experiments/oneoff/heat_flux_timings_n1/"): "zro_schnet_n1.nc",
    Path("/u/mlang//gknet/gknet-jax/experiments/heat_flux_timings/zro/so_n2"): "zro_so_n2.nc",
    Path("/u/mlang//gknet/gknet-jax/experiments/heat_flux_timings/snse/so_n2"): "snse_so_n2.nc",
}


def obtain(result, outfile):
    with open(result / "results.yaml", "r") as f:
        data = yaml.safe_load(f)

    smallest = list(data.keys())[0]

    sizes = np.array(list(data.keys()))
    keys = list(data[smallest].keys())

    arrays = {}

    for name in keys:
        times = np.array([experiment[name]["times"] for experiment in data.values()])
        arrays[name] = xr.DataArray(
            data=times,
            coords={"n_atoms": sizes, "trials": np.arange(times.shape[1])},
            dims=["n_atoms", "trials"],
        )

    dataset = xr.Dataset(arrays)

    dataset.to_netcdf(outfile)


for resultsfile, outfile in tasks.items():
    obtain(resultsfile, outfile)

