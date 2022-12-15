
data = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

with open("data") as f:
    data = f.read()

grid = {}
min_x, max_x = 500, 500
min_y, max_y = 0, 0

def add_line(sx, sy, ex, ey):
    new_min_x, new_max_x = min(sx, ex, min_x), max(sx, ex, max_x)
    new_min_y, new_max_y = min(sy, ey, min_y), max(sy, ey, max_y)
    if sx == ex:
        for y in range(min(sy, ey), max(sy, ey)+1):
            grid[(sx, y)] = 1
    elif sy == ey:
        for x in range(min(sx, ex), max(sx, ex)+1):
            grid[(x, sy)] = 1
    return new_min_x, new_max_x, new_min_y, new_max_y

point_seqs = [[[int(x) for x in point.split(",")] for point in line.split(" -> ")] for line in data.split("\n")]
for point_seq in point_seqs:
    for i, p in enumerate(point_seq[:-1]):
        min_x, max_x, min_y, max_y = add_line(*p, *point_seq[i+1])

grid[(500, 0)] = 3

def get_char(x, y):
    if (x, y) not in grid:
        return "."
    t = grid[(x, y)]
    if t == 1:
        return "#"
    elif t == 2:
        return "o"
    elif t == 3:
        return "+"
    return "?"

def print_grid():
    print("\n".join("".join(get_char(x, y) for x in range(min_x - 10, max_x + 11)) for y in range(min_y, max_y + 3)))

def add_sand():
    x, y = 500, 0
    while y < max_y + 1:
        if (x, y + 1) not in grid:
            y += 1
        elif (x - 1, y + 1) not in grid:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in grid:
            x += 1
            y += 1
        else:
            grid[(x, y)] = 2
            return x != 500 or y != 0
    
    grid[(x, y)] = 2
    return True
        
while add_sand():
    pass

total_sand = sum(t == 2 for t in grid.values())
print(total_sand)
#print_grid()
