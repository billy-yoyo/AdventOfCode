
with open("input") as f:
    lines = f.read().strip().split("\n")

height = len(lines)
width = len(lines[0])

start = tuple([(x, 0) for x, c in enumerate(lines[0]) if c == "."][0])
end = tuple([(x, height - 1) for x, c in enumerate(lines[-1]) if c == "."][0])

def get_c(x, y):
    if 0 <= y < height and 0 <= x < width:
        return lines[y][x]
    
    return "#"

offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]
offset_map = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1)
}

path_lengths = []

stack = [(start, [])]
while stack:
    next_stack = []
    for (x, y), path in stack:
        c = get_c(x, y)
        if c in "<>v^":
            ax, ay = offset_map[c]
            nx, ny = x + ax, y + ay
            if (nx, ny) not in path:
                next_stack.append(((nx, ny), path + [(x, y)]))
        elif (x, y) == end:
            path_lengths.append(len(path))
        else:
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                nc = get_c(nx, ny)
                if (nx, ny) not in path and nc in ".<>v^":
                    next_stack.append(((nx, ny), path + [(x, y)]))

    stack = next_stack


print(max(path_lengths))