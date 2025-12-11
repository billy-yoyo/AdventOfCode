
with open("input") as f:
    input = f.read().strip()

grid = {}

coords, folds = input.split("\n\n")
coords = [tuple(int(x) for x in line.split(",")) for line in coords.split("\n")]
folds = [fold.strip().split(" ")[-1].split("=") for fold in folds.split("\n")]

for coord in coords:
    grid[coord] = True

dims = [max(coords, key=lambda x: x[0])[0] + 1, max(coords, key=lambda x: x[1])[1] + 1]

def fold_grid(axis, value):
    if axis == "x":
        for x, y in list(grid.keys()):
            if x > value:
                grid[((2 * value) - x, y)] = True
                del grid[(x, y)]
        dims[0] = value + 1
    elif axis == "y":
        for x, y in list(grid.keys()):
            if y > value:
                grid[(x, (2 * value) - y)] = True
                del grid[(x, y)]
        dims[1] = value + 1

def print_grid():
    for y in range(dims[1]):
        print("".join(["#" if grid.get((x, y), False) else "." for x in range(dims[0])]))
    print("---")

#print_grid()
for axis, value in folds:
    fold_grid(axis, int(value))
    #print_grid()

print_grid()

#print(sum(1 if grid.get((x, y), False) is True else 0 for x in range(dims[0]) for y in range(dims[1])))
