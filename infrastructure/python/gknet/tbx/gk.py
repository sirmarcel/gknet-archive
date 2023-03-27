"""Tools for working with gk output files"""

# some shortcuts

kk = "heat_flux_autocorrelation_cumtrapz"
kkf = "heat_flux_autocorrelation_cumtrapz_filtered"
kkm = "heat_flux_autocorrelation_cumtrapz_filtered_mean"
kkfm = "heat_flux_autocorrelation_cumtrapz_filtered_mean"
kkfs = "heat_flux_autocorrelation_cumtrapz_filtered_stderr"
khfacff = "heat_flux_autocorrelation_filtered"
khfacffm = "heat_flux_autocorrelation_filtered_mean"
khfacffs = "heat_flux_autocorrelation_filtered_stderr"


def diag(quantity, a):
    if a is not None:
        if quantity.dims == ("time", "a", "b"):
            return quantity.sel(a=a, b=a)
        else:
            return quantity.sel(a=a)
    else:
        return isotropic(quantity)


def isotropic(quantity):
    if quantity.dims == ("time", "a", "b"):
        return (
            quantity.sel(a=0, b=0) + quantity.sel(a=1, b=1) + quantity.sel(a=2, b=2)
        ) / 3
    else:
        return quantity.mean(dim="a")


def get_diagonal(quantity):
    return xr.concat([quantity.sel(a=a, b=a) for a in range(3)], dim="a").transpose()


def get_cutoff(dataset, key=khfacff, a=None, eps=0.0):
    hfacf = diag(dataset[key], a)

    return hfacf.time[hfacf < eps].min()


def get_kappa(dataset, a=None, eps=0.0, filtered=True):
    if filtered:
        suffix = "_filtered_mean"
    else:
        suffix = "_mean"

    key_hfacf = "heat_flux_autocorrelation" + suffix
    key_kappa = "heat_flux_autocorrelation_cumtrapz" + suffix
    key_error = key_kappa.replace("_mean", "_stderr")

    cutoff = get_cutoff(dataset, key_hfacf, a=a, eps=eps)

    k = diag(dataset[key_kappa], a).sel(time=cutoff)
    kerr = diag(dataset[key_error], a).sel(time=cutoff)

    return float(k.data), float(kerr.data)


def trajectory_mean_and_stderr(quantity):
    mean = quantity.mean(dim="trajectory")
    stderr = (quantity.var(dim="trajectory", ddof=1) / len(quantity.trajectory)) ** 0.5

    return mean, stderr


def combine(datasets, add_mean=True, drop_individual=True, diagonal=True, maxtime=5e4):

    if add_mean:
        for k in dataset:
            m, s = get_trajectory_mean(dataset[k])
            dataset.update({k + "_mean": m, k + "_stderr": s})

    if drop_individual:
        for key in dataset:
            if ("_stderr" not in key) and ("_mean" not in key):
                dataset = dataset.drop(key)

    if diagonal:
        for key in dataset:
            dataset[key] = get_diagonal(dataset[key])

    if maxtime:
        dataset = dataset.sel(time=slice(0, maxtime))

    return dataset
