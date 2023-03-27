from tbx import *
from tbx.gk import *
import seaborn as sns


def get_data(temp):
    if temp == 300:
        return load(results / f"kappa_convergence_settings/spacing_m_300_converged.nc")
    else:
        return load(results / f"kappa_convergence_settings/spacing_t_1400_converged.nc")


def get_label(n):
    return str(n)


def plot_spacing(ax, data, spacing, color, x=0, maxsteps=125000, label_offset=0.6):
    plot_mean_kappa(
        ax,
        data.sel(spacing=spacing).dropna(dim="time"),
        color=color,
        alpha_err=0.1,
    )
    cu, kk = plot_cutoff(
        ax,
        data.sel(spacing=spacing),
        color=color,
        kappa=True,
        cutoff=False,
    )
    k, kerr = kk
    t = ax.text(x, k - label_offset, get_label(spacing))
    t.set_bbox(
        {"facecolor": "white", "alpha": 0.8, "edgecolor": None, "boxstyle": "Round"}
    )


fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(colwidth, 9), sharex=False)

settings = {
    300: {
        "xlim": 40e3,
        "ylim": (0, 9.5),
    },
    1400: {
        "xlim": 8e3,
        "ylim": (0, 4.8),
    },
}

for i, temp in enumerate([300, 1400]):
    ax = axs[i]
    s = settings[temp]

    data = get_data(temp)

    positions = 2e0 + np.logspace(1, 3.5, num=10)

    colors = sns.color_palette("flare_r", 9)
    for ii, i in reversed(list(enumerate(range(2, 11)))):
        plot_spacing(
            ax,
            data,
            i,
            colors[ii],
            x=positions[ii + 1],
            label_offset=0.055 * s["ylim"][1],
        )

    plot_spacing(ax, data, 1, black, x=positions[0], label_offset=0.055 * s["ylim"][1])
    ax.set_ylim(*s["ylim"])
    # ax.set_xlim(0, s["xlim"])
    ax.set_title(render_temp(temp))

    ax.set_xlabel("Integration time in fs")
    ax.set_ylabel(kappa_label())
    ax.set_xscale("log", base=10)
    ax.set_xlim(1e1, 5e4)

plt.subplots_adjust(hspace=0.30)
savefig(fig, "preview_spacing.png")
savefig(fig, "../../gknet-paper/img/si-kappa_convergence_spacing.pdf")
