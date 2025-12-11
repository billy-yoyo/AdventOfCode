from collections import defaultdict
from functools import cache

with open("input") as f:
    lines = f.read().strip().split("\n")
  
width = len(lines[0])
height = len(lines)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def step(vec):
    x, y, dir = vec
    ox, oy = offsets[dir]
    return x + ox, y + oy, dir

def bounce(vec):
    x, y, dir = vec
    if x < 0 or x >= width or y < 0 or y >= height:
        return []
    c = lines[y][x]
    if c == ".":
        return [vec]
    elif c == "\\":
        return [(x, y, [WEST, SOUTH, EAST, NORTH][dir])]
    elif c == "/":
        return [(x, y, [EAST, NORTH, WEST, SOUTH][dir])]
    elif c == "|":
        if dir == NORTH or dir == SOUTH:
            return [vec]
        else:
            return [(x, y, NORTH), (x, y, SOUTH)]
    elif c == "-":
        if dir == EAST or dir == WEST:
            return [vec]
        else:
            return [(x, y, EAST), (x, y, WEST)]
    else:
        raise Exception(f"invalid char {c}")

def count_from_start(start):
    hits = defaultdict(bool)
    cache = defaultdict(bool)

    stack = bounce(start)
    while stack:
        new_stack = []
        for vec in stack:
            if cache[vec]:
                continue
            hits[(vec[0], vec[1])] = True
            cache[vec] = True
            new_stack += bounce(step(vec))
        stack = new_stack
    
    return sum(hits.values())

best = 0
for x in range(width):
    best = max(best, count_from_start((x, 0, SOUTH)))
    best = max(best, count_from_start((x, height - 1, NORTH)))

for y in range(height):
    best = max(best, count_from_start((0, y, EAST)))
    best = max(best, count_from_start((width - 1, y, WEST)))


print(count_from_start((0, 0, EAST)))
print(best)
