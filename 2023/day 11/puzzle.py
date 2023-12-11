from collections import defaultdict

enlarge = 1000000 - 1

with open("input") as f:
    galaxies = []
    lines = [x.strip() for x in f.read().strip().split("\n")]
    width = len(lines[0])
    height = len(lines)
    cols = ["".join(line[x] for line in lines) for x in range(width)]
    rx_map = []
    rx = 0
    for col in cols:
        rx_map.append(rx)
        if all(c == "." for c in col):
            rx += enlarge
        rx += 1

    ry = 0
    for y, line in enumerate(lines):
        if all(c == "." for c in line.strip()):
            ry += enlarge + 1
        else:
            for x, c in enumerate(line):
                if c == "#":
                    galaxies.append((rx_map[x], ry))
            ry += 1

def find_quick_distance(i, j):
    start = galaxies[i]
    end = galaxies[j]
    dx = abs(end[0] - start[0])
    dy = abs(end[1] - start[1])
    return dx + dy
    
total = 0
for i in range(len(galaxies)):
    for j in range(i):
        total += find_quick_distance(i, j)

print(total)
