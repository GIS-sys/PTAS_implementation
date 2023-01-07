import numpy as np
from preprocessing import preprocess
from dynamic import do_dp, print_dp_answer


# 1 step is to get input points. For now it is stored in numpy.array `points`

# 0 +.....
# 1 ..+...
# 2 .....+
# 3 ......
# 4 ...+..
#   012345
points = np.array([
    [0, 0],
    [2, 1],
    [3, 4],
    [5, 2],
])
# len of points must be a power of 2, >=4
print("Raw input points:")
print(points)
print("\n")



# 2 step is to preprocess input (described in preprocessing.py)
points_preprocessed = preprocess(points)
print(f"Input points after applying preprocessing:")
print(points_preprocessed)
print("\n")



# 3 step is to do dynamic programming and find exact solution of simplified problem
c = 2**1 # must be 4
m = 2**0 # must be power of 2, ~ log2 (2L) / epsilon

if input("If you want to load recently saved dp - type 'load' and press enter. If you want to recalculate new dp - press anything:\n") == "load":
    with open('dp.txt', 'r') as file_dp:
        dp = eval(file_dp.read())

    with open('dp_answer.txt', 'r') as file_dp_answer:
        dp_answer = eval(file_dp_answer.read())
else:
    dp, dp_answer = do_dp(points_preprocessed, c, m)

    with open('dp.txt', 'w') as file_dp:
        file_dp.write(str(dp.tolist()))

    with open('dp_answer.txt', 'w') as file_dp_answer:
        file_dp_answer.write(str(dp_answer))

    print("Result of dynamic programming:")
    print(f"{dp.shape=}")
    print(dp)
print("|\n")



# 4 step is to recover answer from dp
print(f"Length of found tour: {dp[0][0]}")
print("Used square portal configurations:")
print_dp_answer(points_preprocessed, m, c, dp_answer)
print("\n")



# let's compare answer to real length
from optimal import find_optimal_tour
optimal_tour, optimal_length = find_optimal_tour(points_preprocessed)
print(f"Length of optimal tour: {optimal_length}")
print("Optimal tour:")
print(optimal_tour)

