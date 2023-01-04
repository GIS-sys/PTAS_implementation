import numpy as np


MAX_DP_VAL = 1e18

def iter_leaves(n):
    # return [a, [x, y], 1] where a is index of square, x,y are coordinates of left-upper corner
    L = 4 * n * n
    all_squares = (4 * L * L - 1) // 3
    for i in range(L * L):
        yield [i + all_squares - L * L, [i % L, i // L], 1]

def iter_nonleaves(n):
    # return [a, [x, y], s] where a is index of square, x,y are coordinates of left-upper corner, s is size
    L = int(4 * n * n)
    size = 2
    index = (4 * L * L - 1) // 3 - L * L - 1
    while size < L:
        for y in range(0, L // size):
            for x in range(0, L // size):
                yield [index, [x * size, y * size], size]
                index -= 1
        size *= 2
    yield [0, [0, 0], L]

def iter_portal_usages(m, c):
    # return list of (m*c) numbers between 0 and 2, f. e. [1, 0, 0, 2] for m*c=4
    position = [0] * (4 * m * c)
    index = 0
    while True:
        yield [index, position]
        index += 1
        for k in range(len(position) - 1, -1, -1):
            position[k] += 1
            if position[k] != 3:
                break
            position[k] = 0
        if sum(position) == 0:
            break

def calc_portal_dist_leave(portal_usage, points, square):
    # iterates through all different possibilities of connecting portals 
    #  (according to portal_usage: 0 is not used, 1 is enter, 2 is exit)
    return 1

def check_portal_usage(usage1, usage2, usage3, usage4):
    # check if usages are compatible, i. e. they can be placed next to each other
    mc = len(usage1[1]) // 4
    # top 1-2
    if usage1 and usage2:
        for k in range(0, mc):
            if (usage1[1][mc+k] + usage2[1][3*mc+k]) % 3 != 0:
                return False
    # right 2-4
    if usage2 and usage4:
        for k in range(0, mc):
            if (usage2[1][2*mc+k] + usage4[1][k]) % 3 != 0:
                return False
    # bottom 3-4
    if usage3 and usage4:
        for k in range(0, mc):
            if (usage3[1][mc+k] + usage4[1][3*mc+k]) % 3 != 0:
                return False
    # left 1-3
    if usage1 and usage3:
        for k in range(0, mc):
            if (usage1[1][2*mc+k] + usage3[1][k]) % 3 != 0:
                return False
    return True

def get_parent_portal_usage(usage1, usage2, usage3, usage4):
    # pick sides of usages to form outside of the parent square (combined from 4 smaller ones)
    mc = len(usage1[1]) // 4
    usage = [-1, usage1[1][:mc:2] + usage2[1][:2*mc:2] + usage3[1][mc:3*mc:2] + usage4[1][2*mc:4*mc:2] + usage1[1][3*mc:4*mc:2]]
    usage[0] = get_usage_index(usage)
    return usage

def get_usage_index(usage_without_index):
    # return index for portal usage (x such as [x, [a0, a1, a2, ... amc]] is valid)
    mc = len(usage_without_index[1]) // 4
    index = 0
    for k in range(len(usage_without_index[1])):
        index += usage_without_index[1][-k-1] * (3**k)
    return index

def get_square_index(square_without_index, L):
    # using square[1] = [x, y] and square[2] = size calculate square[0] = index
    level_size = L // square_without_index[2] // 2
    level_index = (4 * level_size * level_size - 1) / 3
    x, y = square_without_index[1]
    x, y = x // square_without_index[2], y // square_without_index[2]
    return int(level_index + x + y * level_size * 2)

def get_children(square, L):
    # return all 4 subsquares on smaller level
    children_size = square[2] // 2
    x, y = square[1]
    children = []
    for dy in [0, 1]:
        for dx in [0, 1]:
            child = [-1, [x + dx * children_size, y + dy * children_size], children_size]
            child[0] = get_square_index(child, L)
            children.append(child)
    return children

def do_dp(points, c, m):
    # create dp[square i][valid visit k] = minimal length of well-behaved tour
    n = len(points)
    L = 4 * n * n
    SQUARES_AMOUNT = (4*L*L-1) // 3 # amount of squares on all levels 1 + 4 + 16 + ... + L*L
    POSITIONS_AMOUNT = 3**(4*m*c) # 2^(2r)=2^(2mc) - how many different possible portal usages
    dp = np.zeros((SQUARES_AMOUNT, POSITIONS_AMOUNT)) + MAX_DP_VAL
    # base
    print("Calculating base for DP...")
    for square in iter_leaves(n):
        for portal_usage in iter_portal_usages(m, c):
            dp[square[0]][portal_usage[0]] = calc_portal_dist_leave(portal_usage, points, square)
    # recursion
    print("Calculating whole DP")
    debug_counter = 0
    for square in iter_nonleaves(n):
        for portal_usage_1 in iter_portal_usages(m, c):
            for portal_usage_2 in iter_portal_usages(m, c):
                debug_counter += 1
                print(f"{debug_counter} / {((4 * L * L - 1) // 3 - L * L) * 3**(4*m*c) * 3**(4*m*c)}")
                if not check_portal_usage(portal_usage_1, portal_usage_2, None, None):
                    continue
                for portal_usage_3 in iter_portal_usages(m, c):
                    if not check_portal_usage(portal_usage_1, portal_usage_2, portal_usage_3, None):
                        continue
                    for portal_usage_4 in iter_portal_usages(m, c):
                        if not check_portal_usage(portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4):
                            continue
                        portal_usage_parent = get_parent_portal_usage(portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4)
                        children = get_children(square, L)
                        new_dp = dp[children[0][0]][portal_usage_1[0]] + dp[children[1][0]][portal_usage_2[0]] + dp[children[2][0]][portal_usage_3[0]] + dp[children[3][0]][portal_usage_4[0]]
                        dp[square[0]][portal_usage_parent[0]] = min(dp[square[0]][portal_usage_parent[0]], new_dp)
    return dp

def get_dp_answer(points, c, m, dp):
    return [points[0], points[1]], dp[0][0]

