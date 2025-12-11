
with open("input") as f:
    input = f.read()

grid = [[int(c) for c in line.strip()] for line in input.strip().split("\n")]
dirs = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0]
width, height = len(grid[0]), len(grid)

def energize(x, y):
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    current = grid[y][x]
    if current == 10:
        return
    elif current == 9:
        grid[y][x] = 10
        for dx, dy in dirs:
            energize(x + dx, y + dy)
    else:
        grid[y][x] = current + 1
    

def step():
    flashes = 0
    for x in range(width):
        for y in range(height):
            energize(x, y)
    
    for x in range(width):
        for y in range(height):
            if grid[y][x] >= 10:
                grid[y][x] = 0
                flashes += 1
    
    return flashes

flashes = 0
i = 0
while flashes < 100:
    flashes = step()
    i += 1

print(i)