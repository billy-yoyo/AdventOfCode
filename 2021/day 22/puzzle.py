

grid = {}

with open("input") as f:
    input = f.read()

lines = [line.strip().split(" ") for line in input.strip().split("\n")]
lines = [[l[0], [[int(y) for y in x.split("=")[1].split("..")] for x in l[1].split(",")]] for l in lines]

def clamp(x):
    return min(max(x, -50), 51)

for mode, ranges in lines:
    xr, yr, zr = ranges
    for x in range(clamp(xr[0]), clamp(xr[1] + 1)):
        for y in range(clamp(yr[0]), clamp(yr[1] + 1)):
            for z in range(clamp(zr[0]), clamp(zr[1] + 1)):
                grid[(x, y, z)] = mode == "on"

print(sum(grid.values()))

