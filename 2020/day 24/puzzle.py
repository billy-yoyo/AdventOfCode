import sys

offsets = {
    "w": (-1, 0),
    "e": (1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
    "sw": (-1, 1),
    "se": (0, 1) 
}

def read_position(pos_string):
    stream = iter(pos_string.strip())
    pos = [0, 0]

    try:
        while True:
            c = next(stream)
            if c in "ns":
                c += next(stream)
            
            off = offsets[c]
            pos[0] += off[0]
            pos[1] += off[1]
    except StopIteration:
        pass

    return tuple(pos)

grid = {}

def flip_tile(pos):
    if pos in grid:
        del grid[pos]
    else:
        grid[pos] = True

def iterate_neighbours(pos):
    for d in ["w", "e", "nw", "ne", "sw", "se"]:
        off = offsets[d]
        yield (pos[0] + off[0], pos[1] + off[1])

def count_neighbours(grid, pos):
    return sum(npos in grid for npos in iterate_neighbours(pos))

def step(grid):
    new_grid = {}

    for pos in grid:
        neighbours = 0
        for npos in iterate_neighbours(pos):
            # white neighour, check if it should turn black
            if npos not in grid:
                neighbour_neighoburs = count_neighbours(grid, npos)
                if neighbour_neighoburs == 2:
                    new_grid[npos] = True
            else:
                neighbours += 1

        if neighbours == 1 or neighbours == 2:
            new_grid[pos] = True
    
    return new_grid

with open("data") as f:
    for line in f:
        pos = read_position(line)
        flip_tile(pos)

for i in range(100):
    grid = step(grid)
print(len(grid))