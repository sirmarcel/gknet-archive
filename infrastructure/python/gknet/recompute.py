from vibes.helpers import progressbar
from vibes.helpers.converters import results2singlepoint
from vibes.trajectory import Trajectory, reader

from .calculator import gknetCalculator
from .vibes_helpers import make_vibes_md


def recompute(trajectory, model, virials_reference=None, virials=True):
    """Recompute trajectory with model"""

    if not isinstance(trajectory, Trajectory):
        original = reader(trajectory)
    else:
        original = trajectory

    calculator = gknetCalculator(
        model, virials=virials, virials_reference=virials_reference, stress=True
    )

    results = []
    for atoms in progressbar(original, prefix="recomputing..."):
        atoms = atoms.copy()
        calculator.calculate(atoms=atoms)
        atoms.calc = results2singlepoint(atoms=atoms, results=calculator.results)
        results.append(atoms)

    trajectory = Trajectory(results, metadata={"calculator": {"name": "gknetCalculator"}})
    trajectory.compute_heat_flux()
    return make_vibes_md(
        trajectory, original=original, timestep=original.timestep, spacing=1
    )
