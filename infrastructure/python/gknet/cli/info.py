import click
from pathlib import Path


@click.group()
def info():
    """info on a vibes-ish result"""


@info.command()
@click.argument("folder", default="predict", type=str)
@click.pass_obj
def predict(obj, folder):
    """info on prediction"""

    from gknet.predict_plot import plot_predictions

    plot_predictions(Path(folder))
