import math


MAX_TOUR_LENGTH = 1e18

def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def find_optimal_tour(points, length=0, visited=[]):
    # simple stupid algorithm, very slow but will find optimal path
    if visited == []:
        points = list([list(point) for point in points])
    if len(points) == 1:
        return ([points[0]], length + dist(visited[-1], points[0]) + dist(points[0], visited[0]))
    min_val = [[], MAX_TOUR_LENGTH]
    for i in range(len(points)-1, -1, -1):
        point = points[i]
        # next recursion step
        points = points[0:i] + points[i+1:]
        visited = visited + [point]
        if len(visited) > 1:
            res = find_optimal_tour(points, length + dist(visited[-2], point), visited)
        else:
            res = find_optimal_tour(points, length, visited)
        if res[1] < min_val[1]:
            min_val = (res[0] + [point], res[1])
        points = points[0:i] + [point] + points[i:]
        visited = visited[:-1]
    return min_val

