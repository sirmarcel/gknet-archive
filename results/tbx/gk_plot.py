from .gk import *
from .plot import *


def setup_ax(ax):
    ax.set_xscale("log", base=10)
    ax.set_xlabel("Integration time in fs")
    ax.set_ylabel("$\kappa$ in W/mK")


def plot_single_kappa(
    ax, kappa, color=black, alpha=1.0, linestyle=solid, label="__nolabel__"
):
    kappa.plot(ax=ax, color=color, alpha=alpha, linestyle=linestyle, label=label)


def plot_mean_kappa(
    ax,
    dataset,
    color=black,
    alpha=1.0,
    alpha_err=0.1,
    linestyle=solid,
    stderr_mult=1.0,
    key=kkf,
    a=None,
    label="__nolabel__",
):
    mean = dataset[key + "_mean"]
    err = stderr_mult * dataset[key + "_stderr"]

    mean = diag(mean, a)
    err = diag(err, a)

    plot_single_kappa(
        ax, mean, color=color, alpha=alpha, linestyle=linestyle, label=label
    )
    ax.fill_between(dataset.time, mean - err, mean + err, alpha=alpha_err, color=color)


def get_cutoff(dataset, key="heat_flux_autocorrelation_filtered_mean", a=None, eps=0.0):
    hfacf = diag(dataset[key], a)
    return hfacf.time[hfacf < eps].min()


def plot_cutoff(
    ax,
    dataset,
    suffix="_filtered_mean",
    a=None,
    color=black,
    alpha=1.0,
    linestyle=solid,
    kappa=False,
    cutoff=True,
    eps=0.0,
):
    key_hfacf = "heat_flux_autocorrelation" + suffix
    key_kappa = "heat_flux_autocorrelation_cumtrapz" + suffix
    cu = get_cutoff(dataset, key_hfacf, a=a, eps=eps)

    if cutoff:
        ax.axvline(
            dataset.time.sel(time=cu), color=color, alpha=alpha, linestyle=linestyle
        )
    k = diag(dataset[key_kappa], a)
    key_error = key_kappa.replace("_mean", "_stderr")
    kerr = diag(dataset[key_error], a)

    if kappa:
        ax.axhline(k.sel(time=cu), color=color, alpha=alpha, linestyle=linestyle)
        ax.fill_between(
            k.time,
            k.sel(time=cu) - kerr.sel(time=cu),
            k.sel(time=cu) + kerr.sel(time=cu),
            color=color,
            alpha=0.1,
            linestyle=linestyle,
        )

    return float(cu), (float(k.sel(time=cu)), float(kerr.sel(time=cu)))


def get_kappa(dataset, suffix="_filtered_mean", a=None, eps=0.0):
    key_hfacf = "heat_flux_autocorrelation" + suffix
    key_kappa = "heat_flux_autocorrelation_cumtrapz" + suffix
    cutoff = get_cutoff(dataset, key_hfacf, a=a, eps=eps)

    k = diag(dataset[key_kappa], a)
    k = k.sel(time=cutoff)
    key_error = key_kappa.replace("_mean", "_stderr")
    kerr = diag(dataset[key_error], a).sel(time=cutoff)

    return float(k.data), float(kerr.data)


def get_colors(n):
    # dark to bright
    c = sns.color_palette("rocket", 3)
    return c, iter(c)


def label(ax, label, pos=(0.1, 0.95)):
    ax.text(
        *pos,
        label,
        fontsize="x-large",
        verticalalignment="center",
        horizontalalignment="center",
        transform=ax.transAxes
    )
