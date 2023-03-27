import io
import numpy as np

from ase.io import write


def xyz_cellh(filename, atoms):
    rotated = orient_atoms(atoms)
    comment = f"# CELL(H):     " + "     ".join([f"{x:.5f}" for x in get_cellh(rotated)])
    comment += r" cell{angstrom}"
    comment += r" positions{angstrom}"

    if filename is None:
        return xyz_to_string(rotated, comment)
    else:
        write(filename, rotated, format="xyz", comment=comment)


def xyz_cellabc(filename, atoms):
    rotated = orient_atoms(atoms)
    comment = f"# CELL(abcABC):     " + "     ".join(
        [f"{x:.5f}" for x in get_cellabc(rotated)]
    )
    comment += r" cell{angstrom}"
    comment += r" positions{angstrom}"

    if filename is None:
        return xyz_to_string(rotated, comment)
    else:
        write(filename, rotated, format="xyz", comment=comment)


def xyz_cellgenh(filename, atoms):
    comment = f"# CELL(GENH):     " + "     ".join(
        [f"{x:.5f}" for x in get_cellgenh(atoms)]
    )
    comment += r" cell{angstrom}"
    comment += r" positions{angstrom}"

    if filename is None:
        return xyz_to_string(atoms, comment)
    else:
        write(filename, atoms, format="xyz", comment=comment)


def orient_atoms(atoms):
    new = atoms.copy()
    new.set_cell(atoms.cell.cellpar())
    new.set_scaled_positions(atoms.get_scaled_positions())

    return new


def get_cellh(atoms):
    return atoms.get_cell().T.flatten()


def get_cellgenh(atoms):
    return atoms.get_cell().flatten()


def get_cellabc(atoms):
    return atoms.get_cell().cellpar()


def xyz_to_string(atoms, comment):

    with io.StringIO() as f:
        write(f, atoms, format="xyz", comment=comment)
        out = f.getvalue()

    return out


# testing


def parse_with_ipi(string):

    with io.StringIO(string) as f:

        from ipi.utils.io.backends import io_xyz

        comment, cell, qatoms, names, masses = io_xyz.read_xyz(f)

    return cell.T, qatoms.reshape((int(len(qatoms) / 3), 3))


def compare_atoms_with_parsed(atoms, cell_and_positions, atol=1e-8):
    cell, positions = cell_and_positions

    return np.allclose(atoms.get_cell(), cell, atol=atol) and np.allclose(
        atoms.get_positions(), positions, atol=atol
    )
