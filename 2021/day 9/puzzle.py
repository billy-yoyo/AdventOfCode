from collections import defaultdict

with open("input") as f:
    input = f.read()

height_map = [[int(c) for c in line.strip()] for line in input.split("\n")]
height = len(height_map)
width = len(height_map[0])

basins = defaultdict(int)
cache = {}
directions = [
    (0, 1), (0, -1), (1, 0), (-1, 0)
]

def find_lowest(start):
    if start in cache:
        return cache[start]
    else:
        start_height = height_map[start[1]][start[0]]
        minx, miny, minh = start[0], start[1], start_height
        for dx, dy in directions:
            x = start[0] + dx
            y = start[1] + dy
            if 0 <= x < width and 0 <= y < height:
                h = height_map[y][x]
                if h < minh:
                    minx, miny, minh = x, y, h
        lowest = (minx, miny)
        if minh < start_height:
            lowest = find_lowest((minx, miny))
        cache[start] = lowest
        if start_height < 9:
            basins[lowest] += 1
        return lowest

def is_low_point(point):
    ph = height_map[point[1]][point[0]]
    for dx, dy in directions:
        x = point[0] + dx
        y = point[1] + dy
        if 0 <= x < width and 0 <= y < height:
            h = height_map[y][x]
            if h <= ph:
                return False
    return True

for y in range(height):
    for x in range(width):
        find_lowest((x, y))
            
sorted_basins = sorted(basins.items(), key=lambda x: x[1], reverse=True)

print(sorted_basins[0][1] * sorted_basins[1][1] * sorted_basins[2][1])

