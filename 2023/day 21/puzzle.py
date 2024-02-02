from functools import cache

with open("example") as f:
    data = f.read().strip().split("\n")

width = len(data[0])
height = len(data)

def get(x, y):
    if is_outside(x, y):
        return "#"
    else:
        c = data[y][x]
        if c == "S":
            return "."
        else:
            return c

def is_outside(x, y):
    return x < 0 or x >= width or y < 0 or y >= height 


offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

@cache
def count_internal(start, steps_remaining):
    fallouts = set()
    stack = {start}
    for i in range(steps_remaining):
        next_stack = set()
        for x, y in stack:
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if is_outside(nx, ny):
                    fallouts |= {(nx % width, ny % height, steps_remaining - (i + 1))}
                elif get(nx, ny) == ".":
                    next_stack |= {(nx, ny)}
        stack = next_stack
    return len(stack), fallouts

MAX_STEPS = 64

initial_start = [(x, y, MAX_STEPS) for y, l in enumerate(data) for x, c in enumerate(l) if c == "S"][0]
stack = [initial_start]
total = 0
for x, y, remaining in stack:
    sub_total, fallouts = count_internal((x, y), remaining)
    total += sub_total
    for fallout in fallouts:
        stack.append(fallout)
    
print(total)
