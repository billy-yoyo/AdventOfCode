from collections import defaultdict

directions = [
    (1, 0),
    (0, 1)
]

with open("input") as f:
    data = f.read().strip().split("\n")

width = len(data[0])
height = len(data)

occupied = defaultdict(bool)

cucumbers = [
    (x, y, c == "v") for y, line in enumerate(data) for x, c in enumerate(line) if c in ">v"
]

for x, y, _ in cucumbers:
    occupied[(x, y)] = True

def step_dir(x, y, dx, dy):
    return (x + dx) % width, (y + dy) % height

def find_moveable(id):
    can_move = []
    for i, (x, y, t) in enumerate(cucumbers):
        if t != id:
            continue

        dx, dy = directions[t]
        nx, ny = step_dir(x, y, dx, dy)
        if occupied[(nx, ny)]:
            continue

        can_move.append(i)
    return can_move

def move(indices):
    for i in indices:
        x, y, t = cucumbers[i]
        dx, dy = directions[t]
        nx, ny = step_dir(x, y, dx, dy)
        cucumbers[i] = (nx, ny, t)
        occupied[(x, y)] = False
        occupied[(nx, ny)] = True

def step():
    east_moving = find_moveable(0)
    move(east_moving)
    south_moving = find_moveable(1)
    move(south_moving)
    return len(east_moving) + len(south_moving) > 0

def print_state():
    lines = [["."] * len(data[0]) for y in range(len(data))]
    for x, y, t in cucumbers:
        lines[y][x] = ">" if t == 0 else "v"
    print("\n".join(["".join(line) for line in lines]))

i = 1
while step():
    i += 1
    pass

print(i)


