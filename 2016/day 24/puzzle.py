import itertools

with open("input") as f:
    data = f.read().strip().split("\n")

offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]

def find_paths_from(index):
    start = [(x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c == str(index)][0]
    path_lengths = {}
    visited = {start}
    stack = [start]
    steps = 0
    while stack:
        next_stack = []
        for x, y in stack:
            if data[y][x] != ".":
                path_lengths[int(data[y][x])] = steps
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if data[ny][nx] != "#" and (nx, ny) not in visited:
                    next_stack.append((nx, ny))
                    visited |= {(nx, ny)}
        stack = next_stack
        steps += 1
    return path_lengths

graph = {}

size = 8

for i in range(size):
    graph[i] = find_paths_from(i)

def walk_length(perm):
    position = 0
    length = 0
    for x in perm:
        length += graph[position][x]
        position = x
    return length + graph[position][0]

best_walk = min(walk_length(perm) for perm in itertools.permutations(range(1, size)))
print(best_walk)
