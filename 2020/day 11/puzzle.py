
grid = {}

with open("data") as f:
    for y, line in enumerate(f.read().split()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

def neighbours(x, y):
    gradients = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for dx, dy in gradients:
        cx, cy = x + dx, y + dy
        while (cx, cy) in grid and grid[(cx, cy)] == ".":
            cx += dx
            cy += dy
        if (cx, cy) in grid:
            yield grid[(cx, cy)]
        else:
            yield "."

def print_grid():
    lines = []
    for x, y in grid:
        while len(lines) <= y:
            lines.append([])
        while len(lines[y]) <= x:
            lines[y].append([])
        lines[y][x] = grid[(x, y)]
    print("\n".join("".join(line) for line in lines))

def step_grid():
    changes = {}
    for x, y in grid:
        c = grid[(x, y)]
        occupied = sum(n == "#" for n in neighbours(x, y))
        if c == "L" and occupied == 0:
            changes[(x, y)] = "#"
        elif c == "#" and occupied >= 5:
            changes[(x, y)] = "L"

    grid.update(changes)
    return len(changes)

def stabilize_grid():
    changes = step_grid()
    while changes > 0:
        changes = step_grid()
    
    return sum(c == "#" for c in grid.values())

print(stabilize_grid())