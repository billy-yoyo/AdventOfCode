
with open("input") as f:
    instructions = [x.split(" ") for x in f.read().strip().split("\n")]
    instructions = [(int(c[2:-2], 16), "RDLU"[int(c[-2])]) for a, b, c in instructions]
    #instructions = [(int(b), a) for a, b, c in instructions]

offsets = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}

vertices = []
cx, cy = 0, 0
lox, loy = 0, 0
for steps, direction in instructions:
    ox, oy = offsets[direction]
    vertices.append((cx, cy))
    cx, cy = cx + (ox * steps), cy + (oy * steps)

perimiter = sum(abs(x0 - vertices[(i+1)%len(vertices)][0]) + abs(y0 - vertices[(i+1)%len(vertices)][1]) for i, (x0, y0) in enumerate(vertices))

area = 0
for i, vert in enumerate(vertices):
    next_vert = vertices[(i + 1) % len(vertices)]
    area += (vert[0] * next_vert[1]) - (vert[1] * next_vert[0])

print(1 + int((area + perimiter) / 2))
