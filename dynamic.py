import numpy as np
import math
from preprocessing import get_L


MAX_DP_VAL = 1e18

def iter_leaves(n):
    # return [a, [x, y], 1] where a is index of square, x,y are coordinates of left-upper corner
    L = get_L(n)
    all_squares = (4 * L * L - 1) // 3
    for i in range(L * L):
        yield [i + all_squares - L * L, [i % L, i // L], 1]

def iter_nonleaves(n):
    # return [a, [x, y], s] where a is index of square, x,y are coordinates of left-upper corner, s is size
    L = get_L(n)
    size = 2
    index = (4 * L * L - 1) // 3 - L * L - 1
    while size < L:
        for y in range(L // size - 1, -1, -1):
            for x in range(L // size - 1, -1, -1):
                yield [index, [x * size, y * size], size]
                index -= 1
        size *= 2
    yield [0, [0, 0], L]

def get_portal_enters_exits_diff(portal_usage):
    portal_enters = sum([1 if x == 1 else 0 for x in portal_usage[1]])
    portal_exits = sum([1 if x == 2 else 0 for x in portal_usage[1]])
    return portal_enters - portal_exits

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


log_counter = 0


def iter_4_correlated_portal_usages(m, c):
    global log_counter
    # return 4 lists of (m*c) numbers between 0 and 2, f. e. [1, 0, 0, 2] for m*c=4, such that they are compatible
    #  (placed side-to-side exits will meet enters of other square)
    mc = m * c
    position = [0] * ((8 * m + 4 * m - 4) * c - 4 + 2 * c) # 8 sides of bigger square, 4 inner sides; -4 because other 4 are calculated from others (enters=exits); +2c for center
    while True:
        log_counter += 1
        portals = []
        # create portals for subsquares #??????????????
        pos = [0] + position[0:2*mc-1] + [0] + position[2*mc-1:4*mc-2] + [0] + position[4*mc-2:6*mc-3] + [0] + position[6*mc-3:]
        portals.append([-1, pos[0:mc] + pos[mc:mc+c][::-1] + pos[8*mc:9*mc-c] + [0] * c + pos[11*mc-3*c:12*mc-4*c][::-1] + pos[7*mc:8*mc]])
        portals.append([-1, pos[mc:2*mc] + pos[2*mc:3*mc] + pos[3*mc:3*mc+c][::-1] + pos[9*mc-c:10*mc-2*c][::-1] + [0] * c + pos[8*mc:9*mc-c][::-1]])
        portals.append([-1, pos[7*mc:7*mc+c][::-1] + pos[11*mc-3*c:12*mc-4*c] + [0]*c + pos[10*mc-2*c:11*mc-3*c] + pos[5*mc:6*mc] + pos[6*mc:7*mc]])
        portals.append([-1, [0] * c + pos[9*mc-c:10*mc-2*c] + pos[3*mc:4*mc] + pos[4*mc:5*mc] + pos[5*mc:5*mc+c][::-1] + pos[10*mc-2*c:11*mc-3*c][::-1]])
        # make them compatible: turn some portals 2->1, 1->2 (0->0)
        transform = lambda x: [0, 2, 1][x]
        for k in range(mc):
            portals[0][1][mc+k] = transform(portals[0][1][mc+k])
            portals[1][1][2*mc+k] = transform(portals[1][1][2*mc+k])
            portals[3][1][3*mc+k] = transform(portals[3][1][3*mc+k])
            portals[2][1][k] = transform(portals[2][1][k])
        # center
        for k in range(0, c):
            portals[0][1][2*c*m + c - 1 - k] = pos[-2*c + k]
        for k in range(0, c // 2):
            portals[1][1][3*c*m + c//2 + k] = transform(pos[-2*c + c//2 + k])
        for k in range(0, c // 2):
            portals[1][1][3*c*m + k] = transform(pos[-2*c + c + k])
        for k in range(0, c//2):
            portals[2][1][c*m + k] = transform(pos[-2 * c + k])
        for k in range(0, c//2):
            portals[2][1][c*m + c//2 + k] = transform(pos[-2 * c + 3 * c//2 + k])
        for k in range(0, c):
            portals[3][1][k] = pos[-2 * c + 2 * c - 1 - k]
        # if enters != exits then skip this
        indexes = [0, 1, 3, 2]
        for k in range(4):
            diff = get_portal_enters_exits_diff(portals[k])
            if diff < 0:
                portals[k][1][indexes[k] * mc] = 1
            if diff > 0:
                portals[k][1][indexes[k] * mc] = 2
        if not (get_portal_enters_exits_diff(portals[0]) or get_portal_enters_exits_diff(portals[1]) or get_portal_enters_exits_diff(portals[2]) or get_portal_enters_exits_diff(portals[3])):
            for k in range(4):
                portals[k][0] = get_usage_index(portals[k])
            yield portals

        for k in range(len(position) - 1, -1, -1):
            position[k] += 1
            if position[k] != 3:
                break
            position[k] = 0
        if sum(position) == 0:
            break

def portal_to_point(portal_index, c, m):
    if portal_index < c * m:
        return [portal_index // c * (1 / m), 0]
    portal_index -= c * m
    if portal_index < c * m:
        return [1, portal_index // c * (1 / m)]
    portal_index -= c * m
    if portal_index < c * m:
        return [1 - portal_index // c * (1 / m), 1]
    portal_index -= c * m
    if portal_index < c * m:
        return [0, 1 - portal_index // c * (1 / m)]
    raise Exception(f"Unexpected {portal=} in portal_to_point")

def calculate_shortest_tour_recursively(portal_usage, c, m, left=-1, right=-1):
    # connect 1 to 2 in portal_usage
    min_distance = MAX_DP_VAL
    if left == -1 and right == -1:
        left = 0
        right = len(portal_usage[1]) - 1
    while left <= right and portal_usage[1][left] == 0:
        left += 1
    while left <= right and portal_usage[1][right] == 0:
        right -= 1
    if left >= right:
        return 0
    k = 1
    direction_to_balance = lambda x: [0, -1, 1][x] # translates 0->0, 1->-1, 2->1
    balance = direction_to_balance(portal_usage[1][left])
    while k <= right - left:
        balance += direction_to_balance(portal_usage[1][left + k])
        if balance == 0:
            point_left = portal_to_point(left, c, m)
            point_right = portal_to_point(left + k, c, m)
            current_distance = math.sqrt((point_left[0] - point_right[0])**2 + (point_left[1] - point_right[1])**2) # distance between left and left+k
            part1 = calculate_shortest_tour_recursively(portal_usage, c, m, left + 1, left + k - 1)
            part2 = calculate_shortest_tour_recursively(portal_usage, c, m, left + k + 1, right)
            min_distance = min(min_distance, part1 + part2 + current_distance)
        k += 1
    if balance != 0:
        return MAX_DP_VAL
    return min_distance

def calc_portal_dist_leave(portal_usage, points, square, c, m):
    # check that portal usage is compatible with points
    # then iterate through all different possibilities of connecting portals 
    #  (according to portal_usage: 0 is not used, 1 is enter, 2 is exit)
    # and find shortest tour
    if get_portal_enters_exits_diff(portal_usage):
        return MAX_DP_VAL
    points_list = [[int(point[0]), int(point[1])] for point in points]
    indexes = [[0, 3], [1, 2]]
    for dx in [0, 1]:
        for dy in [0, 1]:
            point = [int(square[1][0]) + dx, int(square[1][1]) + dy]
            if point in points_list:
                found_portal_on_point = False
                for x in range(0, c):
                    if portal_usage[1][c * m * indexes[dx][dy] + x]:
                        found_portal_on_point = True
                        break
                if not found_portal_on_point:
                    return MAX_DP_VAL
    return calculate_shortest_tour_recursively(portal_usage, c, m)

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

def get_parent_portal_usage(usage1, usage2, usage3, usage4, c, m):
    # pick sides of usages to form outside of the parent square (combined from 4 smaller ones)
    mc = m * c
    usage = []
    usage_x2 = usage1[1][0:m*c] + usage2[1][0:2*m*c] + usage4[1][m*c:3*m*c] + usage3[1][2*m*c:4*m*c] + usage1[1][3*m*c:4*m*c]
    for k in range(0, len(usage_x2) // c, 2):
        for z in range(c):
            usage.append(usage_x2[k*c+z])
    usage = [-1, usage]
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
    global log_counter
    # create dp[square i][valid visit k] = minimal length of well-behaved tour
    n = len(points)
    L = get_L(n)
    SQUARES_AMOUNT = (4*L*L-1) // 3 # amount of squares on all levels 1 + 4 + 16 + ... + L*L
    POSITIONS_AMOUNT = 3**(4*m*c) # 2^(2r)=2^(2mc) - how many different possible portal usages
    dp = np.zeros((SQUARES_AMOUNT, POSITIONS_AMOUNT)) + MAX_DP_VAL
    dp_answer = [[None] * POSITIONS_AMOUNT for _ in range(SQUARES_AMOUNT)]
    # base
    print("Calculating base for DP...")
    for square in iter_leaves(n):
        for portal_usage in iter_portal_usages(m, c):
            dp[square[0]][portal_usage[0]] = calc_portal_dist_leave(portal_usage, points, square, c, m)
        if square[0] % (L * L // 4) == 0:
            print(f"{square[0] - (4 * L * L - 1) // 3 + L * L} / {L * L}")
    # recursion
    print("Calculating whole DP")
    last_log_counter = -1e9
    for square in iter_nonleaves(n):
        for portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4 in iter_4_correlated_portal_usages(m, c):
            portal_usage_parent = get_parent_portal_usage(portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4, c, m)
            #if portal_usage_1[0] == 2*3**3+1*3**2 and portal_usage_2[0] == 2*3**3+1*3**2+2*3**1+1*3**0 and portal_usage_3[0] == 2*3**5+1*3**4 and portal_usage_4[0] == 2*5**3+1*4**2+2*3**7+1*3**6:
            children = get_children(square, L)
            if portal_usage_parent[0] == 0 and portal_usage_1[0] == 0 and portal_usage_2[0] == 0:
                print("$", square, portal_usage_parent, portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4, get_children(square, L))
                print("#", children, dp[children[0][0]][portal_usage_1[0]], dp[children[1][0]][portal_usage_2[0]], dp[children[2][0]][portal_usage_3[0]], dp[children[3][0]][portal_usage_4[0]])
            #if portal_usage_parent[0] == 0:
            #    print("@", square, portal_usage_1[0], portal_usage_2[0], portal_usage_3[0], portal_usage_4[0])
            if get_portal_enters_exits_diff(portal_usage_parent):
                continue
            #if portal_usage_1[0] == 0 and portal_usage_2[0] == 0 and portal_usage_3[0] == 0 and portal_usage_4[0] == 0:
            #if portal_usage_parent[0] == 0:
            #    print("#", children, dp[children[0][0]][portal_usage_1[0]], dp[children[1][0]][portal_usage_2[0]], dp[children[2][0]][portal_usage_3[0]], dp[children[3][0]][portal_usage_4[0]])
            new_dp = dp[children[0][0]][portal_usage_1[0]] + dp[children[1][0]][portal_usage_2[0]] + dp[children[2][0]][portal_usage_3[0]] + dp[children[3][0]][portal_usage_4[0]]
            if new_dp < dp[square[0]][portal_usage_parent[0]]:
                dp[square[0]][portal_usage_parent[0]] = new_dp
                dp_answer[square[0]][portal_usage_parent[0]] = [portal_usage_1, portal_usage_2, portal_usage_3, portal_usage_4]
            if log_counter // 100_000 != last_log_counter // 100_000:
                print(f"{log_counter} / {((4 * L * L - 1) // 3 - L * L) * 3**((8 * m + 4 * m - 4) * c - 4 + 2 * c)}")
            last_log_counter = log_counter
    return dp, dp_answer

#def get_dp_answer_recursively(dp_answer, square, portal_usage, L):
#    if square[2] == 4:
#        print(square, portal_usage)
#        return
#    for k, child in enumerate(get_children(square, L)):
#        get_dp_answer_recursively(dp_answer, child, dp_answer[square[0]][portal_usage[0]][k], L)

def get_dp_answer_recursively(dp_answer, square, portal_usage, L):
    bfs = [[square, portal_usage]]
    while bfs:
        square, portal_usage = bfs[0]
        bfs = bfs[1:]
        print(square, portal_usage)
        if square[2] == 1:
            continue
        for k, child in enumerate(get_children(square, L)):
            bfs.append([child, dp_answer[square[0]][portal_usage[0]][k]])

def get_dp_answer(points, c, m, dp):
    n = len(points)
    L = get_L(n)
    square = [0, [0, 0], L]
    portal_usage = [-1, [0] * 4 * c * m]
    portal_usage[0] == get_usage_index(portal_usage)
    return get_dp_answer_recursively(dp, square, portal_usage, L)

