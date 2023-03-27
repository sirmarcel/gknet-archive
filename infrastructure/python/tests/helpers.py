import numpy as np


def compare_distances(a, b, cutoff, atol=0.0, rtol=1e-7):
    a = filter_and_sort(a, cutoff)
    b = filter_and_sort(b, cutoff)

    np.testing.assert_allclose(a, b, atol=atol, rtol=rtol)


def filter_and_sort(distances, cutoff):
    d = distances[distances < cutoff]
    d = d[d > 0]
    return np.sort(d)
