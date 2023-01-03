from assumptions import make1, make2, make3, make4


# 1 step is to get input points. For now it is simply stored in list `points`

# 0 ......
# 1 .+....
# 2 .....+
# 3 ......
# 4 ....+.
#   012345
points = [
    [1, 1],
    [4, 4],
    [5, 2],
]
print("Raw input points:")
print(points)
print("\n")


# 2 step is to apply several assumptions (described in assumptions.py) to the input

points = make1(points)
points = make2(points)
points = make3(points)
points = make4(points)
print("Input points after applying assumptions:")
print(points)
print("\n")


# 3 step is to ??????????


print(points)

