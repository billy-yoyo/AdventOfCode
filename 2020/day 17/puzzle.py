import time
start_time = time.time()

grid = {}

with open("data") as f:
    for y, line in enumerate(f.read().split()):
        for x, c in enumerate(line):
            if c == "#":
                grid[(x, y, 0, 0)] = True

def is_active(x, y, z, w):
    return (x, y, z, w) in grid

def neighbours(x, y, z, w):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx == dy == dz == dw == 0:
                        continue
                    
                    yield (x + dx, y + dy, z + dz, w + dw)

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

for i in range(6):
    grid = step()

print(len(grid))
end_time = time.time()
print(end_time - start_time)