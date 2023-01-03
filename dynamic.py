import numpy as np


def do_dp(points, c, m):
    # create dp[square i][valid visit k] = minimal length of well-behaved tour
    n = len(points)
    L = 4 * n * n
    SQUARES_AMOUNT = (4*L*L-1) // 3 # amount of squares on all levels 1 + 4 + 16 + ... + L*L
    POSITIONS_AMOUNT = 2**(2*m*c) # 2^(2r)=2^(2mc) - how many different possible portal usages
    dp = np.zeros((SQUARES_AMOUNT, POSITIONS_AMOUNT)) - 1
    print(f"{dp.shape=}")
    return dp

