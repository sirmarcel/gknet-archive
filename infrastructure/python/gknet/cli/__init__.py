import click

from vibes.cli.cli_tracker import CliTracker


@click.group()
@click.pass_context
def gknet(ctx):
    """gknet cli (vibes ripoff edition)"""
    ctx.obj = CliTracker()
    ctx.help_option_names = ["-h", "--help"]


from .run import run
from .submit import submit
from .info import info
from .out import out
from .util import util

gknet.add_command(run)
gknet.add_command(submit)
gknet.add_command(info)
gknet.add_command(out)
gknet.add_command(util)
