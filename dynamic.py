import numpy as np


MAX_DP_VAL = 1e18

def iter_leaves(n):
    yield 0
    return

def iter_nonleaves(n):
    yield 0
    return

def iter_portal_usages(m, c):
    yield 0
    return

def calc_portal_dist_leave(portal_usage, points, square):
    return 1

def check_portal_usage(usage1, usage2, usage3, usage4):
    return True

def get_parent_portal_usage(usage1, usage2, usage3, usage4):
    return 1

def get_children(square):
    return [0, 1, 2, 3]

def do_dp(points, c, m):
    # create dp[square i][valid visit k] = minimal length of well-behaved tour
    n = len(points)
    L = 4 * n * n
    SQUARES_AMOUNT = (4*L*L-1) // 3 # amount of squares on all levels 1 + 4 + 16 + ... + L*L
    POSITIONS_AMOUNT = 3**(2*m*c) # 2^(2r)=2^(2mc) - how many different possible portal usages
    dp = np.zeros((SQUARES_AMOUNT, POSITIONS_AMOUNT)) + MAX_DP_VAL
    # base
    for square in iter_leaves(n):
        for portal_usage in iter_portal_usages(m, c):
            dp[square][portal_usage] = calc_portal_dist_leave(portal_usage, points, square)
    # recursion
    for square in iter_nonleaves(n):
        for portal_usage_1 in iter_portal_usages(m, c):
            for portal_usage_2 in iter_portal_usages(m, c):
                for portal_usage_3 in iter_portal_usages(m, c):
                    for portal_usage_4 in iter_portal_usages(m, c):
                        if check_portal_usage(portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4):
                            portal_usage_parent = get_parent_portal_usage(portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4)
                            children = get_children(square)
                            new_dp = dp[children[0]][portal_usage_1] + dp[children[1]][portal_usage_2] + dp[children[2]][portal_usage_3] + dp[children[3]][portal_usage_4]
                            #dp[square][portal_usage_parent] = min(dp[square][portal_usage], calc_portal_dist_inner(portal_usage, portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4))
                            dp[square][portal_usage_parent] = min(dp[square][portal_usage], new_dp)
    return dp

def get_dp_answer(points, c, m, dp):
    return [points[0], points[1]], dp[0][0]

