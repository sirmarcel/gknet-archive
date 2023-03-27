from ase.io import read, write
from helpers import xyz_cellh

atoms = read("../monoclinic_exp_real_prod_1/cells/300_geometry.in.primitive.supercell_324", format="aims")
xyz_cellh("geometry.xyz", atoms)
write("geometry.in", atoms, format="aims")