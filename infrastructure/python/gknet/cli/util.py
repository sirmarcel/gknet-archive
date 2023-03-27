import click
from pathlib import Path

from vibes.cli.misc import complete_files as paths

from gknet.helpers import talk


@click.group()
def util():
    """various utils"""


@util.command()
@click.argument("model", default=Path("best_model.torch"), type=Path)
@click.argument("geometry", default=Path("geometry.in"), type=Path)
@click.option(
    "-o", "--outfile", default="reference_virials.nc", help="outfile", type=Path
)
@click.option(
    "-d", "--device", default=None, help="device", type=str
)
@click.option(
    "--heat_flux", default="hardy", help="type of heat flux (hardy, fan)", type=str
)
def virials(model, geometry, outfile, device, heat_flux):
    from ase.io import read
    from gknet.experimental.fast_calculator import fastCalculator
    import xarray as xr
    from vibes import dimensions, keys

    if heat_flux == "hardy":
        calc = fastCalculator(model, virials=True, hardy=True, device=device)
        key = keys.virials
    elif heat_flux == "fan":
        calc = fastCalculator(model, virials=True, hardy=False, fan=True, device=device)
        key = "fan_virials"
    else:
        raise ValueError(f"unknown heat flux {heat_flux}")

    atoms = read(geometry, format="aims")
    result = calc.calculate(atoms)

    dataset = xr.DataArray(
        result[key],
        dims=(dimensions.I, dimensions.a, dimensions.b),
        name=keys.virials,
    )

    dataset.to_netcdf(outfile)
