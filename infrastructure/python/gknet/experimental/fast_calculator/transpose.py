import numba
import numpy as np


def get_transpose_idx(idx):
    transpose = np.zeros((*idx.shape[:2], 2), dtype=int)
    return _get_transpose_idx(idx.astype(int), transpose)


def warm_start():
    idx = np.array([[1], [0]])
    transpose = np.zeros((2, 1, 2), dtype=int)
    _get_transpose_idx(idx, transpose)


@numba.jit(nopython=True, cache=True)
def _get_transpose_idx(idx, transpose):
    n, m = idx.shape

    for i in range(n):
        for j in range(m):
            # what entry are we inverting?
            jj = idx[i, j]
            if jj == -1:
                ii = -1
            else:
                ii = find(idx[jj], i)
            transpose[i, j] = [jj, ii]

    return transpose


@numba.jit(nopython=True, cache=True)
def find(array, target):
    n = len(array)
    for i in range(n):
        if array[i] == target:
            return i
    return -1
