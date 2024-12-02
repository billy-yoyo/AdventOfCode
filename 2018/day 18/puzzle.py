
OPEN = 0
LUMBERYARD = 1
TREE = 2
TYPE_MAP = ".#|"

with open("input") as f:
    grid = tuple([tuple([TYPE_MAP.index(c) for c in line]) for line in f.read().strip().split("\n")])

width = len(grid[0])
height = len(grid)

def get(grid, x, y):
    if 0 <= x < width and 0 <= y < height:
        return grid[x][y]
    return OPEN

def new_state(grid, x, y):
    type_counts = [0, 0, 0]
    for ox in range(-1, 2):
        for oy in range(-1, 2):
            if ox == 0 and oy == 0:
                continue
            type_counts[get(grid, x + ox, y + oy)] += 1
    cur = get(grid, x, y)
    if cur == OPEN and type_counts[TREE] >= 3:
        return TREE
    elif cur == TREE and type_counts[LUMBERYARD] >= 3:
        return LUMBERYARD
    elif cur == LUMBERYARD:
        if type_counts[LUMBERYARD] >= 1 and type_counts[TREE] >= 1:
            return LUMBERYARD
        else:
            return OPEN
    return cur

def step(grid):
    return tuple([tuple([new_state(grid, x, y) for x in range(width)]) for y in range(height)])

def calculate_cycle(grid):
    seen_at = {}

    steps = 0
    while True:
        if grid in seen_at:
            first_steps = seen_at[grid]
            return first_steps, steps - first_steps
        seen_at[grid] = steps
        grid = step(grid)
        steps += 1

offset, period = calculate_cycle(grid)
print(offset, period)
cycle_steps = (1000000000 - offset) % period
steps = offset + cycle_steps
for _ in range(steps):
    grid = step(grid)

type_counts = [0, 0, 0]
for x in range(width):
    for y in range(height):
        type_counts[get(grid, x, y)] += 1
print(type_counts)
print(type_counts[LUMBERYARD] * type_counts[TREE])

