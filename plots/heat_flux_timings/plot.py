from tbx import *

from scipy.optimize import curve_fit


develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


def fit_func(x, d, c):
    return d * x + c


def fit_curve(x, y, sigma=None):
    lx = np.log10(x)
    ly = np.log10(y)

    if sigma is None:
        popt, pcov = curve_fit(fit_func, lx, ly, p0=[2.0, 50.0])
    else:
        popt, pcov = curve_fit(fit_func, lx, ly, p0=[2.0, 50.0], sigma=sigma)

    return x, 10 ** fit_func(lx, *popt), popt


def fit(data, key, start=0):
    end = len(data.n_atoms)
    curve_y = data[key].mean(dim="trials").isel(n_atoms=slice(start, end)).data

    return fit_curve(data.isel(n_atoms=slice(start, end)).n_atoms.data, curve_y)


data = xr.open_dataset(results / "heat_flux_timings/zro_schnet_n2.nc")

names = {
    "hardy": "Hardy",
    "unfolded": "Unfolded",
    "virials": "Virials",
    "no_hf": "Forces",
}

label_positions = {
    "hardy": 5e1,
    "unfolded": 5e-1,
    "virials": 1e-1,
    "no_hf": 5e-2,
}


label_rotations = {
    "hardy": 24,
    "unfolded": 8.0,
    "virials": 9.5,
    "no_hf": 10,
}


def plot(ax, data, key, color):
    plot_x, plot_y, params = fit(data, key, start=3)

    if color == black:
        label = r"Fit $\propto N^x$"
    else:
        label = "__nolabel__"

    ax.plot(plot_x, plot_y, color=color, linestyle=solid, alpha=0.8, label=label)

    mean = data[key].mean(dim="trials")
    err = data[key].std(dim="trials")

    # ax.plot(data.n_atoms, mean, color=color, linestyle=solid)
    # ax.fill_between(data.n_atoms, mean - err, mean + err, color=color, alpha=0.1)

    if color == black:
        label = "Data"
    else:
        label = "__nolabel__"

    ax.scatter(
        data.n_atoms,
        mean,
        # yerr=err,
        color=color,
        # linestyle="none",
        marker=bigdot,
        label=label,
    )

    name = names[key]

    show_at = 0

    ax.text(
        plot_x[show_at],
        plot_y[show_at] * 1.5,
        r"name, $\propto N^{X}$".replace("X", f"{params[0]:.1f}").replace("name", name),
        fontsize="large",
        rotation=label_rotations[key],  # can't get an automatic approach to work
    )


fig, ax = fig_and_ax(figsize=(0.95 * colwidth, 3.5))

plot(ax, data, "unfolded", black)
plot(ax, data, "no_hf", teal)
plot(ax, data, "hardy", red)


ax.set_yscale("log", base=10)
ax.set_xscale("log", base=10)
ax.set_ylim(1e-2, 2e3)


ax.legend(loc="upper left", markerfirst=False)

ax.set_xlabel("Number of atoms in simulation cell ($N$)")
ax.set_ylabel("Time in s")

ax.set_xticks(data.n_atoms.data)
ax.set_xticklabels(list(map(str, data.n_atoms.data)))
ax.set_xticks([], minor=True)

# disable the labelled (!!) minor ticks
from matplotlib.ticker import LogLocator

ax.xaxis.set_minor_locator(LogLocator(10, [0]))

savefig(fig, "preview.png")
savefig(fig, img / "heat_flux_timings.pdf")
