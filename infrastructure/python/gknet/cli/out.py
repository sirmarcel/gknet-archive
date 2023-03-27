import click
from pathlib import Path
import xarray as xr
import numpy as np

from vibes import defaults, keys

from stepson.trajectory.derived_properties import getter, add_property


def open_dataset(folder):
    folder = Path(folder)
    if folder.is_file():
        return xr.open_dataset(folder)
    else:
        return xr.open_mfdataset(f"{folder}/*.nc")


@click.group()
def out():
    """out"""


@out.command()
@click.argument("file", default=Path("trajectory.son"), type=Path)
@click.option("-o", "--outfolder", default=None, help="outfolder", type=Path)
@click.option("-b", "--batchsize", default=25000, help="batch size for reading")
@click.option("--full", is_flag=True)
@click.pass_obj
def md(obj, file, outfolder, batchsize, full=False):
    """turn son into dataset"""
    from stepson.comms import comms

    if outfolder is None:
        outfolder = Path(f"trajectory")

    if outfolder.is_dir():
        comms.warn(f"{outfolder} exists, stopping!")
        return None
    else:
        outfolder.mkdir(exist_ok=False)

    from stepson import reader, Reporter

    reporter = comms.reporter()
    reporter.start(f"post-processing {file}")
    for i, dataset in enumerate(
        reader(
            file,
            full=full,
            batch_size=batchsize,
            properties=[keys.temperature, keys.volume],
        )
    ):
        reporter.step(f"saving batch {i}")
        dataset.to_netcdf(outfolder / f"trajectory_{i:05d}.nc")
        reporter.finish_step()

    reporter.done()


@out.command()
@click.argument("folder", default=Path("trajectory/"), type=Path)
@click.option("-o", "--outfile", default="heat_flux.nc", type=Path)
@click.option("--other_virials", default=None, type=Path)
@click.option(
    "--maxsteps",
    default=15000,
    type=int,
    help="cut off dataset after maxsteps for determination of lowest characteristic frequency",
)
@click.option(
    "--freq/--nofreq", default=True, help="compute lowest characteristic frequency"
)
@click.option(
    "--truncate",
    default=False,
    is_flag=True,
    help="truncate heat flux to length of other_virials",
)
@click.option(
    "--spacing",
    default=None,
    type=int,
    help="use every nth timestep (ONLY for other_virials) (see option in gk command)",
)
@click.option(
    "--other_virials_key",
    default=None,
    type=str,
    help="use alternative name for other_virials",
)
def hf(
    folder, outfile, other_virials, maxsteps, freq, truncate, spacing, other_virials_key
):
    """compute heat flux and perform Green-Kubo preparation"""
    import dask

    from stepson.green_kubo import get_heat_flux_dataset
    from stepson.comms import comms

    if outfile.is_file():
        comms.warn(f"{outfile} exists, skipping")
        return None

    with dask.config.set(**{"array.slicing.split_large_chunks": True}):
        reporter = comms.reporter()
        reporter.start(f"working on {folder}")

        reporter.step("open dataset")

        dataset = open_dataset(folder)

        reporter.finish_step()

        if other_virials is not None:
            comms.talk(f"using external virials from {other_virials}", full=True)
            if keys.stresses_potential in dataset:
                comms.talk("found stresses in original dataset, dropping them")
                dataset = dataset.drop(keys.stresses_potential)

            reporter.step(f"getting external virials")
            other = open_dataset(other_virials)

            if spacing is not None:
                comms.talk(
                    f"taking every {spacing}-th step from original dataset", full=True
                )
                dataset = dataset.isel(time=slice(0, len(dataset.time), spacing))

            if len(other.time) != len(dataset.time):
                if not truncate:
                    reporter.done()
                    comms.warn(
                        f"mismatched time axis for recomputed virials: {len(other.time)} != {len(dataset.time)}",
                        full=True,
                    )
                    return None
                else:
                    steps = len(other.time)
                    comms.warn(f"truncating to {steps} WILL NOT CHANGE OUTFILE")
                    dataset = dataset.isel(time=slice(0, steps))

            # check that we have successfully aligned datasets
            assert dataset.time[-1] == other.time[-1]
            assert dataset.time[-2] == other.time[-2]

            if other_virials_key is None:
                if keys.virials in other:
                    dataset = dataset.update(
                        {keys.virials: other[keys.virials]}
                    ).unify_chunks()
                if keys.stresses_potential in other:
                    dataset = dataset.update(
                        {keys.stresses_potential: other[keys.stresses_potential]}
                    ).unify_chunks()
            else:
                comms.talk(f"using virials named {other_virials_key}", full=True)
                dataset = dataset.update(
                    {keys.virials: other[other_virials_key]}
                ).unify_chunks()

            reporter.finish_step()

        heat_flux = get_heat_flux_dataset(
            dataset, steps_for_frequency=maxsteps, include_frequency=freq
        )

        reporter.step(f"write to {outfile}")

        heat_flux.to_netcdf(outfile)

        reporter.done()


@out.command()
@click.argument("file", default=Path("heat_flux.nc"), type=Path)
@click.option("-o", "--outfile", default="greenkubo.nc", type=Path)
@click.option("--outfolder", default=Path("."), type=Path)
@click.option("-w", "--window_factor", default=defaults.window_factor)
@click.option("--total", is_flag=True, help="compute total flux")
@click.option(
    "--maxsteps", default=None, type=int, help="cut off dataset after maxsteps"
)
@click.option("--offset", default=None, type=int, help="start from offset")
@click.option("--spacing", default=None, type=int, help="use only every nth step")
@click.option(
    "--freq", default=None, type=float, help="lowest characteristic frequency"
)
def gk(file, outfile, outfolder, window_factor, total, maxsteps, offset, spacing, freq):
    """perform greenkubo analysis for heat flux dataset in FILE"""
    from stepson.green_kubo import get_kappa_dataset
    from stepson.comms import comms

    reporter = comms.reporter()
    reporter.start(f"working on {file}")
    dataset = xr.open_dataset(file)

    outfolder.mkdir(exist_ok=True)
    outfile = outfolder / outfile

    if offset is not None:
        if offset < 0:
            offset = len(dataset.time) + offset

    if total:
        outfile = outfile.parent / f"{outfile.stem}.total.nc"

    if offset is not None:
        outfile = outfile.parent / f"{outfile.stem}.from_{offset}.nc"

    if maxsteps is not None:
        outfile = outfile.parent / f"{outfile.stem}.to_{maxsteps}.nc"

    if spacing is not None:
        outfile = outfile.parent / f"{outfile.stem}.every_{spacing}.nc"

    if freq is not None:
        outfile = outfile.parent / f"{outfile.stem}.freq_{freq:.2f}.nc"

    if outfile.is_file():
        comms.warn(f"{outfile} exists, skipping")
        reporter.done()
        return None

    if maxsteps is not None:
        comms.talk(f"truncating to {maxsteps} timesteps")

        if len(dataset.time) < maxsteps:
            comms.warn(
                f"Tried to truncate {len(dataset.time)} timesteps to {maxsteps}, but dataset too short."
            )
            reporter.done()
            return None

        dataset = dataset.isel(time=slice(0, maxsteps))

    if offset is not None:
        comms.talk(f"starting from timestep {offset}")
        dataset = dataset.isel(time=slice(offset, len(dataset.time)))

    if spacing is not None:
        comms.talk(f"using spacing {spacing}")
        dataset = dataset.isel(time=slice(0, len(dataset.time), spacing))

    ds_gk = get_kappa_dataset(
        dataset,
        window_factor=window_factor,
        aux=total,
        freq=freq,
    )

    reporter.step(f"write to {outfile}")

    ds_gk.to_netcdf(outfile)

    reporter.done()


@out.command()
@click.argument("file", default="trajectory.son")
@click.option("-r", "--rge", type=int, nargs=3, help="start, stop, step")
def therm(file, rge):
    """pick samples from trajectory"""
    import son
    from stepson.comms import comms
    from vibes.trajectory.io import _create_atoms
    from vibes.filenames import filenames

    reporter = comms.reporter()

    reporter.start(f"extracting samples from {file}")
    metadata, reader = son.open(file)

    pre_atoms_dict = metadata["atoms"]

    rge = list(range(*rge))

    reporter.step(f"reading trajectory", spin=False)
    for i, entry in enumerate(reader):

        if i in rge:
            reporter.tick(f", extract step {i}")
            atoms = create_atoms(entry, pre_atoms_dict)
            info_str = f"Sample no.: {i:7d}"
            atoms.write(
                f"{filenames.atoms}.{i:05d}",
                format="aims",
                info_str=info_str,
                velocities=True,
                scaled=True,
            )

        else:
            reporter.tick(f", skip step {i}")

    reporter.done()


def create_atoms(dct, pre_atoms_dict):
    from vibes.helpers.converters import dict2atoms

    atoms_dict = {**pre_atoms_dict, **dct["atoms"]}

    atoms = dict2atoms(
        atoms_dict,
        calculator_dict=None,
        single_point_calculator=False,
    )

    return atoms


@out.command()
@click.argument("supercell", default=Path("geometry.in.supercell"), type=Path)
@click.argument("folder", default=Path("md/trajectory/"), type=Path)
@click.option("-o", "--outfile", default=None, type=Path)
@click.option("--offset", type=int, default=25000, help="number of steps to drop")
@click.option(
    "-p",
    "--pressure",
    type=float,
    default=10.0,
    help="pressure in bar for sanity checking",
)
def npt(supercell, folder, outfile, offset, pressure):
    """pick samples from trajectory"""
    from ase.io import read, write
    from ase.units import bar

    from stepson.comms import comms

    if outfile is None:
        outfile = supercell.with_suffix(".supercell.npt")

    if outfile.is_file():
        comms.warn(f"{outfile} exists, not doing anything")
        return None

    reporter = comms.reporter()

    reporter.start(f"extracting scaled supercell from {folder}")
    reporter.step("get supercell")
    supercell = read(supercell, format="aims")

    reporter.step("prepare dataset")
    data = open_dataset(folder)
    add_property(data, keys.pressure)
    data = data.isel(time=slice(offset, len(data.time)))

    reporter.step("sanity check pressure")
    mean_pressure = data[keys.pressure].mean().compute().data / bar
    comms.info(f"pressure in NPT: {mean_pressure:.2f}bar")

    if mean_pressure > pressure:
        comms.warn(
            f"pressure in NPT is {mean_pressure:.2f}bar, which is above {pressure:.2f}bar. quitting!"
        )
        return None

    reporter.step("get cell")
    cell = data.cell.mean(dim="time").compute().data

    reporter.step("write output")

    supercell.set_cell(cell, scale_atoms=True)

    temperature = data.temperature.mean().compute().data
    info_str = (
        f"scaled unit cell for T={temperature:.2f}K and pressure={mean_pressure:.2f}bar"
    )
    write(
        outfile,
        supercell,
        format="aims",
        scaled=True,
        velocities=False,
        info_str=info_str,
    )

    reporter.done()


@out.command()
@click.argument("folder", default=Path("trajectory/"), type=Path)
@click.argument("hf", type=Path)
@click.option("--virials", default=None, type=Path)
@click.option("--energies", default=None, type=Path)
@click.option("-o", "--outfile", default="heat_flux.nc", type=Path)
@click.option(
    "--convective",
    default=None,
    type=str,
    help="treat convective flux: 'add' or 'only'",
)
@click.option(
    "--truncate",
    default=False,
    is_flag=True,
    help="truncate trajectory to length of heat flux",
)
@click.option(
    "--spacing",
    default=None,
    type=int,
    help="use every nth timestep of trajectory",
)
def nvhf(folder, hf, virials, energies, outfile, convective, truncate, spacing):
    """collect heat flux from recomputation that does not give virials"""
    import dask

    from ase import units

    from stepson.comms import comms
    from stepson.trajectory import add_property
    from stepson.green_kubo.heat_flux import get_prefactor

    if convective is not None:
        outfile = outfile.parent / f"{outfile.stem}.convective_{convective}.nc"

    if outfile.is_file():
        comms.warn(f"{outfile} exists, skipping")
        return None

    with dask.config.set(**{"array.slicing.split_large_chunks": True}):
        reporter = comms.reporter()
        reporter.start("collecting non-virial heat flux")

        reporter.step("open datasets")

        dataset = open_dataset(folder)
        heat_flux_dataset = open_dataset(hf)

        if spacing is not None:
            comms.talk(
                f"taking every {spacing}-th step from original dataset", full=True
            )
            dataset = dataset.isel(time=slice(0, len(dataset.time), spacing))

        if len(heat_flux_dataset.time) != len(dataset.time):
            if truncate:
                comms.warn(f"truncating to {len(heat_flux_dataset.time)}")
                dataset = dataset.isel(time=slice(0, len(heat_flux_dataset.time)))

        if (dataset.time[-1] != heat_flux_dataset.time[-1]) or (
            dataset.time[-2] != heat_flux_dataset.time[-2]
        ):
            comms.warn(
                f"mismatched trajectory and heat flux timestep/duration, proceed with caution"
            )

        if keys.heat_flux_aux in heat_flux_dataset and virials is not None:
            comms.talk("aux already exists, adding to hf and deleting")
            heat_flux_dataset[keys.heat_flux] += heat_flux_dataset[keys.heat_flux_aux]
            heat_flux_dataset.drop(keys.heat_flux_aux)

        reporter.step("compute volume and temperature")
        add_property(dataset, keys.temperature)
        add_property(dataset, keys.volume)

        volume = dataset[keys.volume].mean().compute().data
        temperature = dataset[keys.temperature].mean().compute().data

        reporter.step("compute prefactor")
        prefactor = get_prefactor(volume, temperature)

        heat_flux_dataset.attrs = {
            "volume": volume,
            "temperature": temperature,
            "prefactor": prefactor,
        }

        if energies is not None:
            reporter.step("getting energies")
            comms.talk("using external energies, will not adjust spacing or truncate")
            comms.talk(f".. opening {energies}")
            external = open_dataset(energies)
            np.testing.assert_allclose(external.time.compute(), dataset.time.compute())
            dataset["energies_potential"] = external["energies_potential"]

        if virials is not None:
            reporter.step("removing aux flux")
            comms.talk(f"taking reference virials from {virials}", full=True)

            virials = open_dataset(virials)[keys.virials]

            velocities = dataset[keys.velocities] * 1000 * units.fs
            heat_flux_aux = (
                (virials * velocities.rename(a="b"))
                .sum(dim="I", skipna=False)
                .sum(dim="b", skipna=False)
                .compute()
            ).rename(keys.heat_flux_aux)
            heat_flux_aux = heat_flux_aux.where(~np.isnan(heat_flux_dataset.heat_flux))

            heat_flux_dataset[
                keys.heat_flux_aux
            ] = heat_flux_aux.transpose()  # otherwise it's (time, a) for some reason

            heat_flux_dataset[keys.heat_flux] = (
                heat_flux_dataset[keys.heat_flux] - heat_flux_aux
            ).rename(keys.heat_flux)

        if convective is not None:
            reporter.step("computing convective flux")
            add_property(dataset, "heat_flux_convective")
            dataset["heat_flux_convective"] = dataset["heat_flux_convective"].compute()

            if convective == "add":
                comms.talk("adding convective flux to heat flux")
                heat_flux_dataset[keys.heat_flux] += dataset["heat_flux_convective"]
            elif convective == "only":
                comms.talk("replacing heat flux with convective flux")
                heat_flux_dataset[keys.heat_flux] = dataset[
                    "heat_flux_convective"
                ].rename(keys.heat_flux)
            else:
                comms.warn("unknown mode for convective flux, doing nothing")

        reporter.step(f"write to {outfile}")

        heat_flux_dataset.to_netcdf(outfile)

        reporter.done()


@getter("energies_kinetic", requires=[keys.momenta])
def get_energies_kinetic(dataset):
    momenta = dataset[keys.momenta]
    velocities = dataset[keys.velocities]
    energies_kinetic = (0.5 * momenta * velocities).sum(dim=("a"))

    return energies_kinetic


@getter("energies", requires=["energies_kinetic"])
def get_energies(dataset):
    return dataset["energies_kinetic"] + dataset["energies_potential"]


@getter("heat_flux_convective", requires=["energies"])
def get_heat_flux_convective(dataset):
    from ase.units import fs

    hf = (dataset[keys.velocities] * 1000 * fs * dataset["energies"]).sum(
        dim="I"
    ) / dataset[keys.volume]
    return hf
