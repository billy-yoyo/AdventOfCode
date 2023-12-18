
with open("example") as f:
    instructions = [x.split(" ") for x in f.read().strip().split("\n")]
    instructions = [(int(c[2:-2], 16), "RDLU"[int(c[-2])]) for a, b, c in instructions]

offsets = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}

vertical_lines = []
horizontal_lines = []
cx, cy = 0, 0
for steps, direction in instructions:
    ox, oy = offsets[direction]
    nx, ny = cx + (ox * steps), cy + (oy * steps)
    line = ((min(cx, nx), min(cy, ny)), (max(cx, nx), max(cy, ny)))
    if nx == cx:
        horizontal_lines.append(line)
    else:
        vertical_lines.append(line)
    cx, cy = nx, ny

area = 0

def find_matching_line(lines, pos):
    for start, end in lines:
        if pos == start or pos == end:
            return (start, end)
    return None

horizontal_lines = sorted(horizontal_lines, key = lambda x: x[0][1])
while horizontal_lines:
    top_line = horizontal_lines.pop(0)
    left = find_matching_line(vertical_lines, top_line[0])
    right = find_matching_line(vertical_lines, top_line[1])

    if left is None or right is None:
        break

    cut_point = min(left[1][1], right[1][1])
    area += (cut_point - top_line[0][1]) * (top_line[1][0] - top_line[0][0])
    removed_lines = [l for l in [left, right] if l[1][1] == cut_point]
    cut_lines = [l for l in [left, right] if l[1][1] != cut_point]
    vertical_lines = [((l[0][0], cut_point), l[1]) if l in cut_lines else l for l in vertical_lines if l not in removed_lines]

    # TODO: join up horizontal lines around the cut point, and cut in half any other vertical lines

print(area)
  