from assumptions import make1, make2, make3, make4

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

points = make1(points)
points = make2(points)
points = make3(points)
points = make4(points)

