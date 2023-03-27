from tbx import *

data_300 = xr.open_dataset(results / "kappa_convergence_N_t/m_300.nc")
data_1400 = xr.open_dataset(results / "kappa_convergence_N_t/t_1400.nc")

times = [0.1, 0.3, 0.5, 0.7, 0.9]

fig, ax = fig_and_ax(figsize=(0.95 * colwidth, 4))


def show_single_point(ax, data, choice, highlight=False, **kwargs):
    n, m = choice
    d = data.sel(n_atoms=n, maxsteps=m)
    k = d.kappa_mean
    e = d.kappa_stderr

    base_position = ls[list(ns).index(n)]
    position = base_position - start + distance * list(maxstepss).index(m)
    _, _, bars = ax.errorbar(
        position,
        [k.data],
        linewidth=0,
        markeredgecolor=black,
        **kwargs,
    )
    if highlight:
        ax.fill_between(
            [0, 50], [k - e] * 2, [k + e] * 2, alpha=0.35, color=kwargs["color"]
        )


production = (1500, 250000)
semi = (768, 125000)

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(colwidth, 8), sharex=False)

for i, dty in enumerate([(data_300, 300, 8.5), (data_1400, 1400, 2.2)]):
    data, temp, ylim = dty

    ax = axs[i]

    ns = data.n_atoms.data[0:-1]
    ls = ns ** (1 / 3)
    maxstepss = data.maxsteps.data

    distance = 0.1  # distance between labels
    start = ((len(maxstepss) - 1) * distance) / 2

    for i_n, n in enumerate(ns):
        base_position = ls[i_n]

        d = data.sel(n_atoms=n)
        k = d.kappa_mean
        e = d.kappa_stderr

        _, _, bars = ax.errorbar(
            (base_position - start) + distance * np.arange(len(maxstepss)),
            k.data,
            yerr=e.data,
            color=black,
            elinewidth=2.0,
            linewidth=3,
            label=nolabel,
        )

        for bar in bars:
            bar.set_alpha(0.4)

    show_single_point(
        ax,
        data,
        (production),
        highlight=True,
        color=red,
        marker=bigdot,
        markersize=11,
        label="Production",
    )
    show_single_point(
        ax,
        data,
        semi,
        highlight=False,
        color=teal,
        marker=thiamond,
        markersize=11,
        label="Light",
    )

    ax.set_xticks(ls)
    ax.set_xticklabels(list(map(str, ns)))
    ax.set_xlabel("Number of atoms ($N^{1/3}$) (offset for simulation time $t$)")
    ax.set_xlim(3.0, 15.5)

    ax.set_ylabel(kappa_label())
    ax.set_ylim(0, ylim)

    ax.legend(loc="lower right", ncol=2)
    ax.set_title(render_temp(temp))

plt.subplots_adjust(hspace=0.40)
savefig(fig, "preview.png")
savefig(fig, "../../gknet-paper/img/kappa_convergence.pdf")
