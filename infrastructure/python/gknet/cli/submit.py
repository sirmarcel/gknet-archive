import click
from vibes.cli.misc import complete_files as paths


_command = lambda c, s: f"gknet run {c} {s}"


def _start(settings_file, name, dry=False):
    """check if settings contain [slurm] and submit"""
    from vibes.settings import Settings
    from vibes.slurm.submit import submit as _submit

    settings = Settings(settings_file=settings_file)
    if "slurm" not in settings:
        raise click.ClickException(f"[slurm] settings not found in {settings_file}")

    dct = settings["slurm"]
    dct["name"] = name

    _submit(dct, command=_command(name, settings_file), dry=dry)


@click.group()
@click.option("--dry", is_flag=True)
@click.pass_obj
def submit(obj, dry):
    """submit a vibes-ish workflow to slurm"""
    obj.dry = dry


@submit.command()
@click.argument("file", default="train.in", type=paths)
@click.pass_obj
def train(obj, file):
    """submit TRAIN task from FILE (default: train.in)"""

    _start(file, "train", dry=obj.dry)


@submit.command()
@click.argument("file", default="train.in", type=paths)
@click.pass_obj
def recompute(obj, file):
    """submit recompute task from FILE (default: recompute.in)"""

    _start(file, "recompute", dry=obj.dry)
