import numpy as np
import math


def preprocess(points):
    # let L = 4*n^2
    n = len(points)
    L = 4 * n * n
    # move and resize points in such way that square [0,L-1]x[0,L-1]
    # is the smallest one which can contain all the points
    # (resizing does not change quality of approximation of the algorithm)
    points -= [min(points[:, 0]), min(points[:, 1])]
    dimension_sizes = [max(points[:, 0]), max(points[:, 1])]
    scaling_factor = (L - 2) / max(dimension_sizes)
    points = points * scaling_factor
    points += [1, 1]
    # round each point in such a way that all points are sitting on the grid
    # with size of [0,L-1]x[0,L-1]
    for i, point in enumerate(points):
        points[i] = [math.floor(point[0]), math.floor(point[1])]
    return points

