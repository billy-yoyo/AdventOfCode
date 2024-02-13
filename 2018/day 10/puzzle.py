from collections import defaultdict

current_positions = set()

velocities = []
positions = []

with open("input") as f:
    for line in f.read().strip().split("\n"):
        left, right = line.strip().split(" v")
        position = tuple([int(x.strip()) for x in left.split("=")[1].strip()[1:-1].split(",")])
        velocity = [int(x.strip()) for x in right.split("=")[1].strip()[1:-1].split(",")]
        index = len(velocities)
        velocities.append(velocity)
        positions.append(position)

current_positions = set(positions)

offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]
def check_finished():
    count = 0
    for x, y in positions:
        has_neighbour = any((x + ox, y + oy) in current_positions for ox, oy in offsets)
        if has_neighbour:
            count += 1
    return (count / len(positions)) > 0.95

hours = 0
while not check_finished():
    new_positions = set()
    for i, ((x, y), (vx, vy)) in enumerate(zip(positions, velocities)):
        positions[i] = (x + vx, y + vy)
        new_positions |= {positions[i]}
    current_positions = new_positions
    hours += 1

minx = min(x for x, _ in positions)
maxx = max(x for x, _ in positions)
miny = min(y for _, y in positions)
maxy = max(y for _, y in positions)

print("\n".join(
    "".join(
        "#" if (x, y) in current_positions else "."
        for x in range(minx - 1, maxx + 2)
    )
    for y in range(miny - 1, maxy + 2)
))
print(hours)

