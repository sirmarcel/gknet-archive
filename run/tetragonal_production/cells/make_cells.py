from ase.io import read, write
from ase.cell import Cell

original = read("aims_tetra.in.primitive", format="aims")


def get_atoms(a, b):
    atoms = original.copy()
    cell = Cell.fromcellpar([a, a, b, 90, 90, 90])
    atoms.set_cell(cell, scale_atoms=True)

    return atoms


params = {
    1400: (5.149175824175825, 5.277747252747253),
    1500: (5.154807692307693, 5.2839285714285715),
    1600: (5.160989010989011, 5.292170329670331),
    1650: (5.164774458619983, 5.2948019774984845),
    1700: (5.1685439560439566, 5.299725274725275),
    1750: (5.171291208791209, 5.302472527472528),
    1800: (5.174038461538462, 5.3052197802197805),
    1900: (5.180494505494506, 5.312362637362638),
    2000: (5.187774725274726, 5.321016483516484),
    2100: (5.196016483516484, 5.329945054945055),
}


for temp, cellpar in params.items():
    atoms = get_atoms(*cellpar)
    write(f"{temp}_geometry.in.primitive", atoms, format="aims", scaled=True)
