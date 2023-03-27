import xarray as xr

enss = [f"{i:02d}" for i in range(11)]


def ensemble(folder, subfolder, file):
    datasets = []
    for ens in enss:
        dataset = ((folder / ens) / subfolder) / file

        datasets.append(xr.open_dataset(dataset))

    return datasets
