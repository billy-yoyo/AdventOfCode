with open("input") as f:
    data = f.read().strip().split("\n")

width = len(data[0])
height = len(data)
initial_start = [(x, y) for y, l in enumerate(data) for x, c in enumerate(l) if c == "S"][0]

def get(x, y):
    c = data[y % height][x % width]
    if c == "S":
        return "."
    else:
        return c

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def count_internal(start, steps_remaining):
    hit_times = dict()

    stack = [start]
    hit_times[start] = 0

    for i in range(steps_remaining):
        next_stack = []
        for x, y in stack:
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if get(nx, ny) == "." and (nx, ny) not in hit_times:
                    hit_times[(nx, ny)] = i + 1
                    next_stack.append((nx, ny))
        stack = next_stack
    
    return sum(1 for k, v in hit_times.items() if v % 2 == steps_remaining % 2)

MAX_STEPS = 26501365
n = 65

x1 = count_internal(initial_start, n)
x2 = count_internal(initial_start, n + width)
x3 = count_internal(initial_start, n + width + width)

gap_1 = x1
gap_2 = x2 - x1
gap_3 = x3 - x2

steps = MAX_STEPS // width
result = gap_1 + (gap_2 * steps) + ((steps * (steps - 1) // 2) * (gap_3 - gap_2))

print(result)
