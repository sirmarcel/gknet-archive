import matplotlib.pyplot as plt
from itertools import cycle
from scipy.stats import t


def fig_and_ax(figsize=None):
    if figsize:
        fig = plt.figure(figsize=figsize, dpi=200)
    else:
        fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = plt.axes()
    return fig, ax


def savefig(fig, file):
    fig.savefig(file, bbox_inches="tight", pad_inches=0.05)


tol_vibrant = [
    "#EE7733",
    "#0077BB",
    "#33BBEE",
    "#EE3377",
    "#CC3311",
    "#009988",
    "#BBBBBB",
    "#000000",
]

tol_muted = [
    "#88CCEE",
    "#44AA99",
    "#117733",
    "#332288",
    "#DDCC77",
    "#999933",
    "#CC6677",
    "#882255",
    "#AA4499",
    "#DDDDDD",
]

main_linestyles = ["solid", "dotted", "dashed", "dashdot", (0, (5, 1))]


def minor_ticks_every(ax, spacing):
    from matplotlib.ticker import MultipleLocator

    ax.xaxis.set_minor_locator(MultipleLocator(spacing))


orange = "#EE7733"
blue = "#0077BB"
cyan = "#33BBEE"
magenta = "#EE3377"
red = "#CC3311"
teal = "#009988"
grey = "#BBBBBB"
black = "#000000"

solid = "solid"
dashed = "dashed"
dotted = "dotted"

cross = "x"
diamond = "D"
star = "*"
dot = "."
bigdot = "o"
square = "s"
thiamond = "d"

# stats
# we use 11 trajectories everywhere for now
tinv = lambda p, df: abs(t.ppf(p / 2, df))
ci_factors = [tinv(1.0 - pp, 11 - 1) for pp in [0.68, 0.95, 0.997]]
ci_68 = ci_factors[0]
ci_95 = ci_factors[1]
