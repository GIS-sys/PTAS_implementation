import numpy as np
from preprocessing import preprocess
from dynamic import do_dp


# 1 step is to get input points. For now it is stored in numpy.array `points`

# 0 +.....
# 1 ......
# 2 .....+
# 3 ......
# 4 ...+..
#   012345
points = np.array([
    [0, 0],
    [3, 4],
    [5, 2],
])
# len of points must be power of 2
print("Raw input points:")
print(points)
print("\n")



# 2 step is to preprocess input (described in preprocessing.py)

points_preprocessed = preprocess(points)
print(f"Input points after applying preprocessing:")
print(points)
print("\n")



# 3 step is to do dynamic programming and find exact solution of simplified problem

c = 2**1 # must be power of 2
m = 2**1 # must be power of 2
result = do_dp(points_preprocessed, c, m)

print("Result of dynamic programming:")
print(result)
print("\n")



# 4 step is to ??????????????////



# let's compare answer to real length

from optimal import find_optimal_tour
print(find_optimal_tour(points))

