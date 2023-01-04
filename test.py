import pytest
from optimal import find_optimal_tour
from dynamic import (
    iter_leaves,
    iter_nonleaves,
    iter_portal_usages,
    calc_portal_dist_leave,
    check_portal_usage,
    get_parent_portal_usage,
    get_children,
)
import math
import numpy as np

EPS = 1e-5


def test_optimal():
    points = np.array([[0, 0], [2, 1], [3, 4], [5, 2]])
    optimal_tour, optimal_length = find_optimal_tour(points)
    assert optimal_tour == [[2, 1], [0, 0], [3, 4], [5, 2]]
    assert abs(optimal_length - math.sqrt(5) - math.sqrt(25) - math.sqrt(8) - math.sqrt(10)) < EPS

def test_iter_leaves():
    n = 2
    L = 4 * n * n
    all_squares = (4 * L * L - 1) / 3
    for i, testing_leave in enumerate(iter_leaves(n)):
        if i == 0:
            assert testing_leave == [all_squares - L * L, [0, 0]]
        if i == 1:
            assert testing_leave == [all_squares - L * L + 1, [1, 0]]
        if i == L * L - 1:
            assert testing_leave == [all_squares - 1, [L - 1, L - 1]]
    assert i == L * L - 1

