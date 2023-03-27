from tbx import *
from tbx.gk import *


def get_data(thermo):
    return load(
        results
        / f"kappa_convergence_settings/convective_{thermo}_converged.nc"
    )


def delta_kappa(value):
    k = render_kappa(value, develop=False)
    return r"$\sim$ X".replace("X", k)


def setup_ax(ax, ylim=(0, 10), xlim=30e3):
    minor_ticks_every(ax, 1000)
    scale_labels(ax, 1000)
    ax.set_xlabel("Integration time in ps")
    ax.set_xlim(0, xlim)

    major_ticks_every(ax, 1, direction="y")

    if ylim[1] >= 5:
        minor_ticks_every(ax, 0.5, direction="y")
    else:
        minor_ticks_every(ax, 0.1, direction="y")

    ax.set_ylabel(kappa_label())
    ax.set_ylim(ylim)

    ax.set_title(None)


def plot_difference(ax, a, b):
    cu_a, ke_a = plot_cutoff(ax, a, cutoff=False, kappa=False)
    cu_b, ke_b = plot_cutoff(ax, b, cutoff=False, kappa=False)

    # print(a.time)
    loc = cu_a
    k_a = ke_a[0]
    k_b = ke_b[0]

    lower = min(k_a, k_b)
    upper = max(k_a, k_b)
    padding = max(0.03 * upper, 0.08)
    diff = np.abs(k_b - k_a)
    percentage = (diff / upper) * 100
    print(f"Difference in %: {percentage:.0f}")

    ax.plot([loc, loc], [lower + padding, upper - padding], color=black, linewidth=1)
    ax.text(loc * 1.05, 0.5 * (k_a + k_b) - 0.1, delta_kappa(np.abs(k_b - k_a)))


settings = {
    "m_300": {
        "xlim": 40e3,
        "ylim": (0, 8.5),
    },
    "t_1400": {
        "xlim": 5e3,
        "ylim": (0, 2.2),
    },
    # "m_1400": {
    #     "xlim": 8e3,
    #     "ylim": (0, 2.2),
    # },
}

# jfan_mpnn
# jfan
# jhardy
# junf

js = ["j", "jint", "jpot", "jconv"]
labels = {
    "j": render_j(),
    "jint": render_j(text="int"),
    "jpot": render_j(text="pot"),
    "jconv": render_j(text="conv"),
}

styles = {
    "j": {"color": red, "linestyle": solid, "linewidth": 6},
    "jint": {"color": black, "linestyle": dotted, "linewidth": 3},
    "jpot": {"color": teal, "linestyle": solid, "linewidth": 3},
    "jconv": {"color": orange, "linestyle": dashed, "linewidth": 3},
}


fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(0.98 * colwidth, 9.0), sharex=False)

ax_300, ax_1400 = axs

for i, ts in enumerate(settings.items()):
    thermo, s = ts
    ax = axs[i]
    data = get_data(thermo)

    kappas = {j: data.sel(heat_flux=j) for j in js}

    for j, kappa in kappas.items():
        plot_mean_kappa(
            ax, kappa, key=kk, label=labels[j], alpha_err=0.1, total=False, **styles[j]
        )

    # plot_difference(ax, kappas["junf"], kappas["jfan"])

    setup_ax(ax, **s)
    ax.legend(loc="center right", handlelength=5)

    ax.set_title(render_temp(thermo.split("_")[1]))


plt.subplots_adjust(hspace=0.30)
savefig(fig, "convective.png")
savefig(fig, "../../gknet-paper/img/heat_flux_convective.pdf")
