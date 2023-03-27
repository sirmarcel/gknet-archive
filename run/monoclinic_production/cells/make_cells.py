from ase.io import read, write
from ase.cell import Cell

original = read("aims_monoc.in.primitive", format="aims")


def get_atoms(a, b, c, angle):
    atoms = original.copy()
    cell = Cell.fromcellpar([a, b, c, 90, angle, 90])
    atoms.set_cell(cell, scale_atoms=True)

    return atoms


params = {
    # 300: [5.147, 5.220, 5.324, 99.3], # misread -- closer to Verdi et al. calc. 2.5% diff to actual value.
    300: [5.147, 5.209, 5.311, 99.3],
    350: [5.150, 5.209, 5.315, 99.28],
    400: [5.152, 5.211, 5.318, 99.27],
    450: [5.154, 5.211, 5.322, 99.26],
    600: [5.161, 5.213, 5.330, 99.166],
    750: [5.165, 5.213, 5.340, 99.073],
    900: [5.172, 5.215, 5.349, 98.99],
    1050: [5.179, 5.216, 5.356, 98.86],
    1200: [5.193, 5.237, 5.386, 98.74],
    1400: [5.196, 5.219, 5.388, 98.687]
}

for temp, cellpar in params.items():
    atoms = get_atoms(*cellpar)
    write(f"{temp}_geometry.in.primitive", atoms, format="aims", scaled=True)
