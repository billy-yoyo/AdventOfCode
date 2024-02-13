from collections import deque, defaultdict

horz_lines = []
vert_lines = []

SAND = 0
CLAY = 1
WATER = 2
FLOWING = 3

with open("input") as f:
    for line in f.read().strip().split("\n"):
        a, b = [v.strip() for v in line.split(",")]
        if a.startswith("x"):
            x, y = a[2:], b[2:]
        else:
            x, y = b[2:], a[2:]
        if ".." in x:
            sx, ex = [int(a) for a in x.split("..")]
            horz_lines.append(((sx, ex), int(y)))
        else:
            sy, ey = [int(a) for a in y.split("..")]
            vert_lines.append((int(x), (sy, ey)))

grid = defaultdict(int)
for (sx, ex), y in horz_lines:
    for x in range(sx, ex + 1):
        grid[(x, y)] = CLAY
for x, (sy, ey) in vert_lines:
    for y in range(sy, ey + 1):
        grid[(x, y)] = CLAY


maxx = max(x for x, _ in grid)
minx = min(x for x, _ in grid)
maxy = max(y for _, y in grid)
miny = min(y for _, y in grid)

def print_grid():
    with open("map", "w") as f:
        f.write("\n".join(
            "".join(
                ".#~|"[grid[(x, y)]]
                for x in range(minx, maxx + 1)
            )
            for y in range(miny, maxy + 1)
        ))

def is_clay(x, y):
    return grid[(x, y)] == CLAY

def is_ground(x, y):
    return grid[(x, y)] in (CLAY, WATER)


flow_stack = deque([(500, miny)])
while flow_stack:
    x, y = flow_stack.popleft()
    if y > maxy:
        continue

    if grid[(x, y)] == WATER:
        flow_stack.append((x, y - 1))
        continue

    #print(x, y)
    grid[(x, y)] = FLOWING
    if grid[(x, y + 1)] == SAND:
        flow_stack.append((x, y + 1))
    elif grid[(x, y + 1)] in (CLAY, WATER):
        left, right = x - 1, x + 1
        while not is_clay(left, y) and is_ground(left, y + 1):
            left -= 1
        while not is_clay(right, y) and is_ground(right, y + 1):
            right += 1

        #print(f"{y=} {left=} {right=}")
        
        if not is_clay(left, y):
            grid[(left, y)] = FLOWING

            if grid[(left, y + 1)] != FLOWING:
                flow_stack.append((left, y + 1))
        if not is_clay(right, y):
            grid[(right, y)] = FLOWING

            if grid[(right, y + 1)] != FLOWING:
                flow_stack.append((right, y + 1))
        if is_clay(left, y) and is_clay(right, y):
            for cx in range(left + 1, right):
                grid[(cx, y)] = WATER
            flow_stack.append((x, y - 1))
        else:
            for cx in range(left + 1, right):
                grid[(cx, y)] = FLOWING
                

print_grid()
print(len([x for x in grid.values() if x in (WATER, FLOWING)]))
print(len([x for x in grid.values() if x in WATER]))

