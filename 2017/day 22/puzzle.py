from collections import defaultdict

activated = defaultdict(bool)
state = defaultdict(int)

with open("input") as f:
    data = f.read().strip().split("\n")

init_width = len(data[0])
init_height = len(data)

start = (init_width // 2, init_height // 2, 0)

for y, line in enumerate(data):
    for x, c in enumerate(line):
        activated[(x, y)] = c == "#"
        state[(x, y)] = 2 if c == "#" else 0

directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

count = [0]

def step(pointer):
    x, y, rotation = pointer
    if activated[(x, y)]:
        rotation = (rotation + 1) % 4
    else:
        rotation = (rotation - 1) % 4
    
    if not activated[(x, y)]:
        count[0] += 1
    activated[(x, y)] = not activated[(x, y)]

    dx, dy = directions[rotation]
    return (x + dx, y + dy, rotation)

def step_2(pointer):
    x, y, rotation = pointer
    current_state = state[(x, y)]

    if current_state == 0:
        rotation = (rotation - 1) % 4
    elif current_state == 2:
        rotation = (rotation + 1) % 4
    elif current_state == 3:
        rotation = (rotation + 2) % 4

    if current_state == 1:
        count[0] += 1
    state[(x, y)] = (current_state + 1) % 4

    dx, dy = directions[rotation]
    return (x + dx, y + dy, rotation)

pos = start
for _ in range(10000000):
    pos = step_2(pos)

print(count[0])


