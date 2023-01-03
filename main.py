import numpy as np
from preprocessing import preprocess



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
print("Raw input points:")
print(points)
print("\n")



# 2 step is to preprocess input (described in preprocessing.py)

N = len(points)
points = preprocess(points, N)
print(f"Input points after applying preprocessing (with {N=}):")
print(points)
print("\n")



# 3 step is to apply dynamic programming and solve simplified problem

c = 1
m = 1


print(points)

