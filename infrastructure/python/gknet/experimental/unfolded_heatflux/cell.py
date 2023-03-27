import numpy as np
from collections import namedtuple

# basis: the original cell object
# normals: the normal vectors of the unit cell surfaces (pointing inwards)
#          since each surface is spanned by two basis vectors, only one points
#          out of that surface. normals are indexed such that they match.
# heights: the distance of the basis vector pointing out of each surface
Cell = namedtuple("Cell", ("basis", "normals", "heights"))

def get_cell(cell):
    from ase.cell import Cell as aseCell
    cell = aseCell(cell)
    normals = get_normal_vectors(cell)
    heights = get_heights(cell, normals)

    return Cell(cell, normals, heights)

def get_normal_vectors(cell):
    reciprocal = cell.reciprocal()
    normals = reciprocal / np.linalg.norm(reciprocal, axis=1)[:, None]
    return normals

def get_heights(cell, normals):
    return np.diag(cell @ normals.T)
