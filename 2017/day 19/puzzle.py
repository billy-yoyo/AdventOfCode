

with open("input") as f:
    data = f.read().split("\n")

width = len(data[0])
height = len(data)

start_x = next(x for x, c in enumerate(data[0]) if c == "|")
start = (start_x, 0)

visited = []

offsets = [(0, 1, "- "), (0, -1, "- "), (-1, 0, "| "), (1, 0, "| ")]

def step(last_pos, pos):
    lx, ly = last_pos
    x, y = pos
    dx, dy = x - lx, y - ly
    char = data[y][x]
    if char == "+":
        for ox, oy, not_char in offsets:
            nx, ny = x + ox, y + oy
            if 0 <= nx < width and 0 <= ny < height and (nx != lx or ny != ly) and data[ny][nx] not in not_char:
                return (nx, ny)
    elif char != " ":
        if char not in "|-":
            visited.append(char)
        return (x + dx, y + dy)

last_pos = start
pos = (start_x, 1)
steps = 0
while pos is not None:
    next_pos = step(last_pos, pos)
    steps += 1
    last_pos, pos = pos, next_pos

print("".join(visited), steps)
