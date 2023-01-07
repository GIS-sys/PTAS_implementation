import pytest
from optimal import find_optimal_tour
from preprocessing import get_L
from dynamic import (
    iter_leaves,
    iter_nonleaves,
    iter_portal_usages,
    calc_portal_dist_leave,
    check_portal_usage,
    get_parent_portal_usage,
    get_children,
    MAX_DP_VAL,
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
    n = 4
    L = get_L(n)
    all_squares = (4 * L * L - 1) / 3
    for i, testing_leave in enumerate(iter_leaves(n)):
        if i == 0:
            assert testing_leave == [all_squares - L * L, [0, 0], 1]
        if i == 1:
            assert testing_leave == [all_squares - L * L + 1, [1, 0], 1]
        if i == L * L - 1:
            assert testing_leave == [all_squares - 1, [L - 1, L - 1], 1]
    assert i == L * L - 1

def test_iter_nonleaves():
    n = 4
    L = get_L(n)
    all_squares = (4 * L * L - 1) / 3
    leaves_amount = L * L
    for i, testing_square in enumerate(iter_nonleaves(n)):
        if i == 0:
            assert testing_square == [all_squares - leaves_amount - 1, [2, 2], 2]
        if i == 1:
            assert testing_square == [all_squares - leaves_amount - 2, [0, 2], 2]
        if i == all_squares - leaves_amount - 1:
            assert testing_square == [0, [0, 0], L]
    assert i == all_squares - leaves_amount - 1

def test_get_children():
    n = 4
    L = get_L(n)
    L2 = L // 2
    L4 = L // 4
    assert get_children([0, [0, 0], L], L) == [[1, [0, 0], L2], [2, [L2, 0], L2], [3, [0, L2], L2], [4, [L2, L2], L2]]
    assert get_children([2, [L2, 0], L2], L) == [[7, [L2, 0], L4], [8, [L2+L4, 0], L4], [11, [L2, L4], L4], [12, [L2+L4, L4], L4]]
    assert get_children([4, [L2, L2], L2], L) == [[15, [L2, L2], L4], [16, [L2+L4, L2], L4], [19, [L2, L2+L4], L4], [20, [L2+L4, L2+L4], L4]]

def test_iter_portal_usages():
    m = 3
    c = 2
    for i, testing_portal in enumerate(iter_portal_usages(m, c)):
        if i == 0:
            assert testing_portal == [0, [0] * (4*m*c - 4) + [0, 0, 0, 0]]
        if i == 2:
            assert testing_portal == [2, [0] * (4*m*c - 4) + [0, 0, 0, 2]]
        if i == 6:
            assert testing_portal == [6, [0] * (4*m*c - 4) + [0, 0, 2, 0]]
        if i == 25:
            assert testing_portal == [25, [0] * (4*m*c - 4) + [0, 2, 2, 1]]
            break

def test_get_parent_portal_usage_cm_big():
    usage1 = [-1, [1, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0]]
    usage2 = [-1, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    usage3 = [-1, [0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0]]
    usage4 = [-1, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0]]
    usage_res = [-1, [1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0]]
    assert get_parent_portal_usage(usage1, usage2, usage3, usage4, 2, 2)[1] == usage_res[1]

#def test_get_parent_portal_usage_cm_1():
#    usage1 = [-1, [1, 2, 0, 2]]
#    usage2 = [-1, [1, 0, 0, 0]]
#    usage3 = [-1, [1, 0, 1, 2]]
#    usage4 = [-1, [0, 0, 0, 2]]
#    usage_res = [-1, [1, 0, 0, 2]]
#    assert get_parent_portal_usage(usage1, usage2, usage3, usage4, 1, 1)[1] == usage_res[1]

def test_calc_portal_dist_leave():
    # 1
    portal_usage = [0, [1, 2, 2, 1, 2, 1, 1, 2]]
    points = np.array([[0, 0], [25, 12], [37, 50], [63, 25]])
    n = len(points)
    L = get_L(n)
    square = [(4 * L * L - 1) // 3, [L-1, L-1], 1]
    distance = calc_portal_dist_leave(portal_usage, points, square, c=1, m=2)
    assert distance == 0.5 + 0.5 + 0.5 + 0.5
    # 2
    portal_usage = [0, [0, 0, 2, 1, 2, 1, 1, 2]]
    points = np.array([[0, 0], [2, 2], [1, 2], [3, 3]])
    n = len(points)
    L = get_L(n)
    square = [(4 * L * L - 1) // 3, [L-1, L-1], 1]
    distance = calc_portal_dist_leave(portal_usage, points, square, c=1, m=2)
    assert distance == MAX_DP_VAL
    # 3
    portal_usage = [0, [1, 0, 2, 2, 0, 1, 0, 0]]
    points = np.array([[0, 0], [2, 2], [1, 2], [3, 3]])
    n = len(points)
    L = get_L(n)
    square = [(4 * L * L - 1) // 3, [L-1, L-1], 1]
    distance = calc_portal_dist_leave(portal_usage, points, square, c=1, m=2)
    assert distance == 1 + math.sqrt(0.5)

