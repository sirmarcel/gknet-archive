from tbx import *
from tbx.gk import *
import seaborn as sns

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False

data_300 = load(results / f"kappa_convergence_settings/freq_m_300_converged.nc")
data_1400 = load(results / f"kappa_convergence_settings/freq_t_1400_converged.nc")


def get_label(freq):
    if develop:
        return f"{freq:.2f}"
    else:
        return r"$\qty{X}{THz}$".replace("X", f"{freq:.1f}")


def plot_freq(ax, data, freq, style):
    color, linestyle = style
    plot_mean_kappa(
        ax,
        data.sel(freq=freq).dropna(dim="time"),
        color=color,
        alpha_err=0.1,
        label=get_label(freq),
        linestyle=linestyle,
    )
    cu, kk = plot_cutoff(
        ax,
        data.sel(freq=freq),
        color=color,
        kappa=True,
        cutoff=False,
        linestyle=linestyle,
        alpha_err=0,
    )


fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(colwidth, 9), sharex=True)

freqs = {
    0.3: (red, solid),
    0.5: (orange, dashed),
    1.0: (black, dotted),
    2.0: (teal, dashdot),
    3.0: (blue, loosedot),
    # 5.0: (teal, dashdot),
    # 30.0: (blue, loosedot)
}

ax = axs[0]

for freq, style in reversed(list(freqs.items())):
    plot_freq(ax, data_300, freq, style)

ax = axs[1]
for freq, style in reversed(list(freqs.items())):
    plot_freq(ax, data_1400, freq, style)

ax = axs[-1]
ax.set_xlim(1e1, 5e4)
ax.set_xscale("log", base=10)

for ax in axs:
    ax.set_xlabel("Integration time in fs")
    ax.set_ylabel(kappa_label(develop=develop))
    ax.legend(loc="lower right")

axs[0].set_title(render_temp(300, develop=develop))
axs[1].set_title(render_temp(1400, develop=develop))

savefig(fig, "preview_freq.png")
savefig(fig, "../../gknet-paper/img/si-kappa_convergence_freq.pdf")
