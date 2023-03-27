import click
from pathlib import Path

from vibes.cli.misc import complete_files as paths

from gknet.helpers import talk
from gknet.train import TrainContext
from gknet.predict import PredictContext


@click.group()
def run():
    """run a vibes-ish workflow"""


@run.command()
@click.argument("file", default="train.in", type=paths)
@click.option("--workdir", default=Path("train"), help="working directory")
@click.pass_obj
def train(obj, file, workdir):
    """run training from FILE (default: train.in)"""
    from vibes.settings import Settings

    context = TrainContext(Settings(settings_file=file), workdir=workdir)

    context.run()


@run.command()
@click.argument("file", default="predict.in", type=paths)
@click.option("--workdir", default=Path("predict"), help="working directory")
@click.pass_obj
def predict(obj, file, workdir):
    """run prediction from FILE (default: predict.in)"""
    from vibes.settings import Settings

    context = PredictContext(Settings(settings_file=file), workdir=workdir)

    context.run()


@run.command()
@click.argument("file", default="recompute.in", type=paths)
@click.option("--workdir", default=Path("recompute"), help="working directory")
@click.pass_obj
def recompute(obj, file, workdir):
    """run recomputation from FILE"""
    from vibes.settings import Settings
    from gknet.recompute import RecomputeContext

    context = RecomputeContext(Settings(settings_file=file), workdir=workdir)

    context.run()
