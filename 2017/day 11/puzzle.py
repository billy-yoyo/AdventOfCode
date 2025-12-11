
offsets = {
    "n": (0, -2),
    "s": (0, 2),
    "ne": (1, -1),
    "sw": (-1, 1),
    "se": (1, 1),
    "nw": (-1, -1)
}

def step(pos, direction):
    x, y = pos
    ox, oy = offsets[direction]
    return (x + ox, y + oy)

def step_path(pos, path):
    for dir in path:
        pos = step(pos, dir)
    return pos

def sign(x):
    return -1 if x < 0 else 1

def length(pos):
    mini = min(abs(pos[0]), abs(pos[1]))
    maxi = max(abs(pos[0]), abs(pos[1]))

    off = maxi - mini
    if maxi == pos[1]:
        off //= 2

    return mini + off

def max_distance(pos, path):
    furthest = length(pos)
    for dir in path:
        pos = step(pos, dir)
        furthest = max(length(pos), furthest)
    return furthest

with open("input") as f:
    data = f.read().strip().split(",")

pos = step_path((0, 0), data)
print(pos)
print(length(pos))
print(max_distance((0, 0), data))
