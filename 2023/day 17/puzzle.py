from functools import cache

with open("input") as f:
    lines = f.read().strip().split("\n")

heat_map = [[int(x) for x in line] for line in lines]

width = len(lines[0])
height = len(lines)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]

lowest = {}

def insert_sort(lst, x):
    for i, y in enumerate(lst):
        if x[2] < y[2]:
            break
    else:
        i = len(lst)
    
    lst.insert(i, x)

def dfs():
    path = [(0, 0)]
    last_dir = None
    steps = 0
    heat = 0
    while path[-1] != (width - 1, height - 1):
        choices = []
        for new_dir in range(4):
            if last_dir is not None and (new_dir + 2) % 4 == last_dir:
                continue

            if last_dir is not None and new_dir == last_dir and steps >= 3:
                continue

            new_steps = steps + 1 if last_dir is not None and new_dir == last_dir else 1
            
            ox, oy = offsets[new_dir]
            nx, ny = path[-1][0] + ox, path[-1][1] + oy
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            heat_cost = heat_map[ny][nx]
            choices.append((nx, ny, new_dir, new_steps, heat_cost))
        
        x, y, last_dir, steps, cost = min(choices, key = lambda c: (width - c[0], height - c[1]))
        path += [(x, y)]
        heat += cost
    
    return heat


@cache
def pathfind(x, y, direction, steps, limit=None):

    best_heat = None
    for new_dir in [EAST, SOUTH, WEST, NORTH]:
        if (new_dir + 2) % 4 == direction:
            continue

        if new_dir == direction and steps >= 3:
            continue

        new_steps = steps + 1 if new_dir == direction else 1
        ox, oy = offsets[new_dir]
        nx, ny = x + ox, y + oy
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            continue
            
        cur_heat = pathfind(nx, ny, new_dir, new_steps, limit=best_heat) + heat_map[ny][nx]
        if best_heat is None or cur_heat < best_heat:
            best_heat = cur_heat
    return best_heat


heat_limit = dfs()
print(heat_limit)

stack = [(0, 0, 0, EAST, 0), (0, 0, 0, SOUTH, 0)]
while stack:
    x, y, heat, direction, steps = stack.pop(0)
    print(x, y)
    for new_dir in range(4):
        if (new_dir + 2) % 4 == direction:
            continue

        if new_dir == direction and steps >= 3:
            continue

        new_steps = steps + 1 if new_dir == direction else 1
        ox, oy = offsets[new_dir]
        nx, ny = x + ox, y + oy
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            continue

        new_heat = heat + heat_map[ny][nx]
        if new_heat >= heat_limit:
            continue

        low_key = (nx, ny, new_steps)
        if low_key in lowest and lowest[low_key] < new_heat:
            continue

        lowest[low_key] = new_heat

        if nx != width - 1 or ny != height - 1:
            insert_sort(stack, (nx, ny, new_heat, new_dir, new_steps))
        else:
            print(f"found end heat: {new_heat}")

bottom_right = [v for k, v in lowest.items() if k[0] == width - 1 and k[1] == height - 1]
best_heat = min(bottom_right)
print(best_heat)
