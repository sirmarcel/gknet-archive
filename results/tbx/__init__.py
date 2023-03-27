from pathlib import Path

basedir = Path("/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/")
resultsdir = Path("/Users/marcel/base/desk/phd/projects/gknet/gknet-results/data")


def load_data(file):
    file = Path(file)
    if file.suffix == ".nc":
        import xarray as xr

        return xr.open_dataset(file)
    elif file.suffix == ".npz":
        import numpy as np

        return np.load(file, allow_pickle=True)
    else:
        raise IOError(f"cannot open file {file}")


def get_and_concatenate(getter, quantity, name):
    import xarray as xr
    data = [getter(q) for q in quantity]
    data = xr.concat(data, dim=xr.DataArray(data=quantity, name=name, dims=(name)))

    return data
