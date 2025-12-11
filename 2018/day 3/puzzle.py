from collections import defaultdict

with open("input") as f:
    lines = [x.split("@") for x in f.read().strip().split("\n")]

claims = [(lhs.strip()[1:], rhs.strip().split(":")) for lhs, rhs in lines]
claims = [(id, [int(x) for x in pos.strip().split(",")], [int(x) for x in dims.strip().split("x")]) for (id, (pos, dims)) in claims]

def axis_overlaps(x0, w0, x1, w1):
    return x0 <= x1 + w1 - 1 and x1 <= x0 + w0 - 1

def rect_overlap(p0, d0, p1, d1):
    for i in range(2):
        if not axis_overlaps(p0[i], d0[i], p1[i], d1[i]):
            return False
    return True

def calculate_axis_overlap(x0, w0, x1, w1):
    if axis_overlaps(x0, w0, x1, w1):
        return min(x0 + w0, x1 + w1) - max(x0, x1)
    return 0

def calculate_overlap(p0, d0, p1, d1):
    total = 1
    for i in range(2):
        total *= calculate_axis_overlap(p0[i], d0[i], p1[i], d1[i])
    return total

def get_axis_overlap(x0, w0, x1, w1):
    return (max(x0, x1), min(x0 + w0, x1 + w1))

def get_overlap(p0, d0, p1, d1):
    overlaps = [get_axis_overlap(p0[i], d0[i], p1[i], d1[i]) for i in range(2)]
    return (
        (overlaps[0][0], overlaps[1][0]),
        (overlaps[0][1], overlaps[1][1])
    )

count = 0
overlaps = defaultdict(int)
hit = set()
for i, (id, pos, dims) in enumerate(claims):
    for j in range(i):
        other_id, other_pos, other_dims = claims[j]
        if rect_overlap(pos, dims, other_pos, other_dims):
            (minx, miny), (maxx, maxy) = get_overlap(pos, dims, other_pos, other_dims)
            overlaps[id] += 1
            overlaps[other_id] += 1
            for x in range(minx, maxx):
                for y in range(miny, maxy):
                    hit |= {(x, y)}

print(len(hit))
for id, _, _ in claims:
    if overlaps[id] == 0:
        print(id)
