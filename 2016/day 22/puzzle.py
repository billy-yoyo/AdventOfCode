import re

with open("input") as f:
    lines = f.read().strip().split("\n")

nodes = {}

for line in lines[2:]:
    data = [x for x in line.split() if x]
    _, x_tag, y_tag = data[0].split("-")
    x, y = int(x_tag[1:]), int(y_tag[1:])

    size, used, avail = [int(x[:-1]) for x in data[1:4]]
    nodes[(x, y)] = (size, used, avail)

node_list = list(nodes.keys())

def get_valid_pairs():
    valid_pairs = 0

    for key_a, node_a in nodes.items():
        for key_b, node_b in nodes.items():
            if key_a == key_b:
                continue

            if node_a[1] > 0 and node_a[1] <= node_b[2]:
                valid_pairs += 1
    return valid_pairs

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
def path_to(start, end):
    visited = set()
    steps = 0
    stack = [start]
    while stack:
        next_stack = []
        for x, y in stack:
            if (x, y) == end:
                return steps
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if (nx, ny) in nodes and (nx, ny) not in visited and nodes[(nx, ny)][0] <= 100:
                    visited |= {(nx, ny)}
                    next_stack.append((nx, ny))
        stack = next_stack
        steps += 1
    return None

width = max(x for x, _ in node_list) + 1
height = max(y for _, y in node_list) + 1

start = (width - 1, 0)
end = (0, 0)

start_node = nodes[start]

empty = [key for key, (size, used, avail) in nodes.items() if used == 0][0]


print("\n".join([
    "".join("_" if (x, y) == empty else ("x" if (x, y) == end else ("#" if (x, y) == start else ("#" if nodes[(x, y)][0] > 100 else "."))) for x in range(width)) for y in range(height)
]))


empty_node_distance = path_to(empty, (start[0] - 1, start[1])) #abs(empty[0] - (start[0] - 1)) + abs(empty[1] - start[1])
print(f"{start=} {end=} {empty=} {empty_node_distance}")

steps_distance = (start[0] - 1) * 5

print(empty_node_distance + steps_distance + 1)
