

with open("input") as f:
    lines = [x.split(" ") for x in f.read().strip().split("\n")]
    lines = [(a, int(b), c[1:-1]) for a, b, c in lines]

start = (0, 0)

offsets = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}

hits = set()

def print_set(s):
    print("\n".join("".join("#" if (x, y) in s else "." for x in range(min(x[0] for x in s), max(x[0] for x in s) + 1)) for y in range(min(x[1] for x in s), max(x[1] for x in s) + 1)))

cx, cy = start
for direction, steps, colour in lines:
    ox, oy = offsets[direction]
    for i in range(steps):
        hits |= {(cx, cy)}
        cx, cy = cx + ox, cy + oy

print(len(hits))

int_seed = (1, 1)
stack = [(1, 1)]
while stack:
    new_stack = []
    for x, y in stack:
        for d in "RLUD":
            ox, oy = offsets[d]
            nx, ny = x + ox, y + oy
            if (nx, ny) not in hits:
                hits |= {(nx, ny)}
                new_stack.append((nx, ny))
    stack = new_stack

print(len(hits))



