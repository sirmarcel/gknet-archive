import numpy as np
from vibes.trajectory import Trajectory, reader
import ase.units as u


def get_metadata(timestep, calculator={}, atoms={}):

    md = {"fs": u.fs, "dt": timestep * u.fs}

    return {"MD": md, "calculator": calculator, "atoms": atoms}


def make_vibes_md(trajectory, timestep=4, original=None, spacing=1):
    if not isinstance(trajectory, Trajectory):
        trajectory = reader(trajectory)

    meta = get_metadata(timestep, calculator=trajectory.metadata.get("calculator", {}))

    if original is not None:
        if not isinstance(original, Trajectory):
            original = reader(original)

    for i, atoms in enumerate(trajectory):
        atoms.info.update({"nsteps": i, "dt": timestep * u.fs})

        if original is not None:
            og = original[i * spacing]
            np.testing.assert_allclose(
                atoms.get_positions(), og.get_positions(), rtol=0, atol=1e-15
            )
            np.testing.assert_allclose(
                atoms.get_cell(), og.get_cell(), rtol=0, atol=1e-15
            )

    return Trajectory(trajectory, metadata=meta)
