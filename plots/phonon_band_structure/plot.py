from tbx import *

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


def name(cutoff, t):
    if not develop:
        return r"$T=Y$, $r_{\text{c}}=\SI{X}{\angstrom}$".replace(
            "X", f"{cutoff:.1f}"
        ).replace("Y", str(t))
    else:
        return f"$T = {t}$, $r_c = {cutoff:.1f}$Å"


datadir = results / "phonons"


def setup(ax, ref_phonons):
    setup_bandstructure(ax[0], ref_phonons)
    setup_dos(ax[1])


def setup_bandstructure(ax, phonons):
    all_distances = phonons["bs_all_distances"]
    labels = phonons["bs_labels"]
    if not develop:
        labels = [l.replace("|", r"$\vert$") for l in labels]

    special_points = phonons["bs_special_points"]

    ax.axhline(y=0, linestyle=":", linewidth=0.5, color="black")

    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_tick_params(which="both", direction="in")
    ax.yaxis.set_tick_params(which="both", direction="in")

    ax.set_ylabel("Frequency in THz")
    ax.set_xlabel("Wave vector")

    ax.set_xticks(special_points)
    ax.set_xticklabels(labels, rotation="35")

    ax.set_xlim(0, all_distances[-1][-1])
    ax.set_ylim(-2, 25)


def setup_dos(ax):
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_tick_params(which="both", direction="in")
    ax.yaxis.set_tick_params(which="both", direction="in")

    ax.set_xlabel("Density of states")
    # ax.set_ylabel("Frequency")

    ax.grid(True)
    ax.set_xlim((0, 4))


def plot(ax, phonons, color, linestyle, label):
    plot_bandstructure(ax[0], phonons, color, linestyle, label)
    plot_dos(ax[1], phonons, color, linestyle, label)


def plot_bandstructure(ax, phonons, color, linestyle, label):
    all_distances = phonons["bs_all_distances"]
    all_frequencies = phonons["bs_all_frequencies"]

    for i, df in enumerate(zip(all_distances, all_frequencies)):
        distances, frequencies = df
        for j, freqs in enumerate(frequencies.T):
            if i == 0 and j == 0:
                ax.plot(
                    distances,
                    freqs,
                    color=color,
                    linestyle=linestyle,
                    label=label,
                    alpha=0.75,
                )
            else:
                ax.plot(distances, freqs, color=color, linestyle=linestyle, alpha=0.75)


def plot_dos(ax, phonons, color, linestyle, label):
    frequency_points = phonons["dos_frequency_points"]
    total_dos = phonons["dos_total_dos"]

    ax.plot(
        total_dos,
        frequency_points,
        # linewidth=2,
        color=color,
        linestyle=linestyle,
        alpha=0.75,
        # label=label,
    )


n = 324

aims = load(datadir / f"tetra_aims_n{n}.npz")
schnet = load(datadir / f"tetra_schnet_5.0_n2_n{n}.npz")

fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    gridspec_kw={"width_ratios": [3, 1]},
    sharey=True,
    figsize=(2 * 3.375, 2 * 2),
    dpi=200,
)


ax1, ax2 = ax
setup(ax, aims)
plot(ax, aims, black, solid, "FHI-aims")
plot(ax, schnet, red, solid, "SchNet")
fig.legend(loc="upper center", ncol=3)

savefig(fig, "preview_tetra.png")
savefig(fig, f"../../gknet-paper/img/si-phonons_tetra.pdf")


aims = load(datadir / f"mono_aims_n{n}.npz")
schnet = load(datadir / f"mono_schnet_5.0_n2_n{n}.npz")

fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    gridspec_kw={"width_ratios": [3, 1]},
    sharey=True,
    figsize=(2 * 3.375, 2 * 2),
    dpi=200,
)


ax1, ax2 = ax
setup(ax, aims)
plot(ax, aims, black, solid, "FHI-aims")
plot(ax, schnet, red, solid, "SchNet")
fig.legend(loc="upper center", ncol=3)

savefig(fig, "preview_mono.png")
savefig(fig, f"../../gknet-paper/img/si-phonons_mono.pdf")
