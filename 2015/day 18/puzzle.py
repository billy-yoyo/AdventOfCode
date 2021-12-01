grid = {}

maxy, maxx = 0, 0
with open("data") as f:
    for y, line in enumerate(f.read().split()):
        maxy = y
        for x, c in enumerate(line):
            maxx = x
            if c == "#":
                grid[(x, y)] = True

stuck = {(0, 0): True, (0, maxy): True, (maxx, 0): True, (maxx, maxy): True}

def is_active(x, y):
    return (x, y) in grid or (x, y) in stuck

def neighbours(x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            
            if 0 <= x + dx <= maxx and 0 <= y + dy <= maxy:
                yield (x + dx, y + dy)

def step():
    new_grid = {}
    considered = grid.copy()
    todo = [cell for cell in grid]

    while todo:
        new_todo = []
        for cell in todo:
            if is_active(*cell):
                count = 0
                for neighbour in neighbours(*cell):
                    if neighbour not in considered:
                        new_todo.append(neighbour)
                        considered[neighbour] = True
                    if is_active(*neighbour):
                        count += 1
                
                if 2 <= count <= 3:
                    new_grid[cell] = True
            else:
                count = sum(is_active(*neighbour) for neighbour in neighbours(*cell))
                if count == 3:
                    new_grid[cell] = True
        todo = new_todo
    return new_grid

def print_grid(size):
    print("\n".join("".join(".#"[is_active(x, y)] for x in range(size)) for y in range(size)))
    print("")

for i in range(100):
    grid = step()

print(sum(is_active(x, y) for x in range(maxx + 1) for y in range(maxy + 1)))