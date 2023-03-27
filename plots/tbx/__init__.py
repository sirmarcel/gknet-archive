import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import xarray as xr

from .literals import *
from .stats import *

plt.style.use("../gknet-paper.mlpstyle")

results = Path("/Users/marcel/base/desk/phd/projects/gknet/gknet-results/data")
img = Path("../../gknet-paper/img")
tables = Path("../../gknet-paper/table")


def load(file):
    file = Path(file)
    if file.suffix == ".nc":
        return xr.open_dataset(file)
    elif file.suffix == ".npz":
        return np.load(file, allow_pickle=True)
    else:
        raise IOError(f"cannot open file {file}")


def savefig(fig, file):
    fig.savefig(file, bbox_inches="tight", pad_inches=0.05)


def fig_and_ax(figsize=None):
    if figsize:
        fig = plt.figure(figsize=figsize, dpi=200)
    else:
        fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = plt.axes()
    return fig, ax


def minor_ticks_every(ax, spacing, direction="x"):
    from matplotlib.ticker import MultipleLocator

    if direction == "x":
        ax.xaxis.set_minor_locator(MultipleLocator(spacing))
    else:
        ax.yaxis.set_minor_locator(MultipleLocator(spacing))


def major_ticks_every(ax, spacing, direction="x"):
    from matplotlib.ticker import MultipleLocator

    if direction == "x":
        ax.xaxis.set_major_locator(MultipleLocator(spacing))
    else:
        ax.yaxis.set_major_locator(MultipleLocator(spacing))


def scale_labels(ax, scale, direction="x"):
    from matplotlib.ticker import FuncFormatter

    ticks = FuncFormatter(lambda x, pos: "{0:g}".format(x / scale))

    if direction == "x":
        ax.xaxis.set_major_formatter(ticks)
    else:
        ax.yaxis.set_major_formatter(ticks)


colwidth = 2 * 3.375
