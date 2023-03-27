from tbx import *

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


t = "temperature"
k = "kappa"
e = "error"

raghavan = load(results / "kappa_reference/result_raghavan.npz")
mevrel = load(results / "kappa_reference/result_mevrel.npz")
hasselman = load(results / "kappa_reference/result_hasselman.npz")
bisson = load(results / "kappa_reference/result_bisson.npz")
verdi = load(results / "kappa_reference/result_verdi.npz")
cc = load(results / "kappa_reference/result_cc.npz")

cu5_n2_mono_exp = load(results / "kappa_monoclinic_experiment/result_cu5_n2.nc")
cu5_n2_tetra_exp = load(results / "kappa_tetragonal_experiment/result_cu5_n2.nc")

# unused
# cu5_n2_mono_aims = load(results / "kappa_monoclinic_aims/result_cu5_n2.nc")
# cu5_n2_tetra_schnet = load(results / "kappa_tfl/result_cu5_n2.nc")

fig, ax = fig_and_ax(figsize=(0.98*colwidth, 4.5))


# ax.scatter(
#     [hasselman[t][0]],
#     [hasselman[k][0]],
#     color=black,
#     marker=pentagon,
#     alpha=0.7,
#     label="Hasselman et al. (exp., tetr.)",
#     s=[300],
# )

# ax.scatter(
#     [hasselman[t][0]],
#     [hasselman[k][0]],
#     color=black,
#     marker=diamond,
#     alpha=0.7,
#     label="Hasselman et al. (exp.) (tetragonal)",
# )

# ax.scatter(
#     [hasselman[t][1]],
#     [hasselman[k][1]],
#     color=black,
#     marker=pentagon,
#     alpha=0.7,
#     label="Hasselman et al. (exp.) (monoclinic)",
# )

ax.scatter(
    raghavan[t],
    raghavan[k],
    color=black,
    marker=bigdot,
    alpha=0.7,
    label="Raghavan et al. (exp.) (m)",
    # markersize=12,
)

ax.errorbar(
    mevrel[t],
    mevrel[k],
    color=black,
    marker=cross,
    alpha=0.7,
    yerr=mevrel[e],
    linestyle="none",
    elinewidth=1,
    label="Mévrel et al. (exp.) (m)",
    markersize=9,
)


ax.errorbar(
    bisson[t],
    bisson[k],
    yerr=bisson[e],
    color=black,
    marker=diamond,
    alpha=0.7,
    label="Bisson et al. (exp.) (m)",
    elinewidth=1,
    linestyle="none",
    markersize=9,
)


ax.errorbar(
    cc[t],
    cc[k],
    color=orange,
    marker=plus,
    alpha=0.7,
    yerr=cc[e],
    linestyle="none",
    elinewidth=1,
    label="Carbogno et al. (DFT) (t)",
    markersize=10,
    markeredgecolor=black,
)


ax.errorbar(
    verdi[t],
    verdi[k],
    color=teal,
    marker=square,
    alpha=0.7,
    yerr=verdi[e],
    linestyle="none",
    elinewidth=1,
    label="Verdi et al. (MLP) (m,t)",
    markersize=10,
    markeredgecolor=black,
)


# ax.errorbar(
#     cu5_n2_tetra_schnet[t],
#     cu5_n2_tetra_schnet["kappa_mean"],
#     yerr=cu5_n2_tetra_schnet["kappa_stderr"],
#     color=red,
#     marker=star,
#     elinewidth=1,
#     linestyle="none",
#     alpha=0.9,
#     label="SchNet (MLP, tetragonal)",
#     markersize=15,
#     markeredgecolor=red,
#     )

# ax.errorbar(
#     [cu5_n2_mono_aims[t][0]],
#     [cu5_n2_mono_aims["kappa_mean"][0]],
#     yerr=[cu5_n2_mono_aims["kappa_stderr"][0]],
#     color=red,
#     marker=pentagon,
#     elinewidth=1,
#     linestyle="none",
#     alpha=0.9,
#     label="SchNet (MLP) (monoclinic)",
#     markersize=12,
#     )

ax.errorbar(
    cu5_n2_mono_exp[t],
    cu5_n2_mono_exp["kappa_mean"],
    yerr=cu5_n2_mono_exp["kappa_stderr"],
    color=red,
    marker=thiamond,
    elinewidth=1,
    linestyle="none",
    alpha=0.9,
    label="This work (MLP) (m)",
    markersize=13,
    markeredgecolor=black,
    )

ax.errorbar(
    cu5_n2_tetra_exp[t],
    cu5_n2_tetra_exp["kappa_mean"],
    yerr=cu5_n2_tetra_exp["kappa_stderr"],
    color=red,
    marker=dot,
    elinewidth=1,
    linestyle="none",
    alpha=0.9,
    label="This work (MLP) (t)",
    markersize=19,
    markeredgecolor=black,
    )


handles, labels = ax.get_legend_handles_labels()

# we want tetragonal to be plotted on top, but
# want the legend to be in the opposite order :clown:
handles[-2], handles[-1] = handles[-1], handles[-2]
labels[-2], labels[-1] = labels[-1], labels[-2]

ax.legend(reversed(handles), reversed(labels), loc="upper right", markerfirst=False)

# ax.set_ylim(1, 9.5)
ax.set_ylim(0, 10.5)
ax.set_xlim(200, 1850)

ax.set_xlabel("Temperature in K")
if develop:
    ax.set_ylabel(r"$\kappa$ in W/mK")
else:
    ax.set_ylabel(r"$\kappa$ in \unit{W\per(m.K)}")

minor_ticks_every(ax, 50)
major_ticks_every(ax, 150)

# minor_ticks_every(ax, 50, direction="y")
major_ticks_every(ax, 1, direction="y")


savefig(fig, "preview.png")
savefig(fig, img / "kappa_vs_temperature.pdf")


# def print_at_300(dataset, name=""):
#     k = float(dataset["kappa_mean"].sel(temperature=300))
#     e = float(dataset["kappa_stderr"].sel(temperature=300))
#     print(f"{name:>10} @ 300K: {k:.2f}±{e:.3f}")

# print_at_300(cu5_n2_tetra_schnet, "tetra")
# print_at_300(cu5_n2_mono_exp, "mono")

