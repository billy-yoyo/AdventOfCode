
def overlap(p1, p2):
    return p1[0] <= p2[1] and p2[0] <= p1[1]

def inside(p1, p2):
    return p2[0] <= p1[0] and p1[1] <= p2[1]

def get_range_overlap(p1, p2):
    if overlap(p1, p2):
        return max(p1[0], p2[0]), min(p1[1], p2[1])
    else:
        return None

def get_overlap(c1, c2):
    if all(overlap(p1, p2) for p1, p2 in zip(c1, c2)):
        return [get_range_overlap(p1, p2) for p1, p2 in zip(c1, c2)]
    else:
        return None

# remove p1 from p2
def get_range_exclusion(p1, p2):
    # p1 is inside p2
    if inside(p1, p2):
        if p1[0] == p2[0] and p1[1] == p2[1]:
            return []
        elif p1[0] == p2[0]:
            return [(p1[1] + 1, p2[1])]
        elif p1[1] == p2[1]:
            return [(p2[0], p1[0] - 1)]
        else:
            return [(p2[0], p1[0] - 1), (p1[1] + 1, p2[1])]
    # p2 is inside p1, so exclude everything
    elif inside(p2, p1):
        return []
    elif overlap(p1, p2):
        # p1 overlaps p2 to the left
        if p1[0] < p2[0]:
            return [(p1[1] + 1, p2[1])]
        else:
            return [(p2[0], p1[0] - 1)]
    else:
        [p2]

# remove c1 from c2
def get_exclusion(c1, c2):
    if all(overlap(p1, p2) for p1, p2 in zip(c1, c2)):
        cubes = []
        minx, miny, minz = c2[0][0], c2[1][0], c2[2][0]
        maxx, maxy, maxz = c2[0][1], c2[1][1], c2[2][1]
        x_exclusions = get_range_exclusion(c1[0], c2[0])
        for x1, x2 in x_exclusions:
            cubes.append([(x1, x2), (miny, maxy), (minz, maxz)])
            if x1 == minx:
                minx = x2 + 1
            if x2 == maxx:
                maxx = x1 - 1
        y_exclusions = get_range_exclusion(c1[1], c2[1])
        for y1, y2 in y_exclusions:
            cubes.append([(minx, maxx), (y1, y2), (minz, maxz)])
            if y1 == miny:
                miny = y2 + 1
            if y2 == maxy:
                maxy = y1 - 1
        z_exclusions = get_range_exclusion(c1[2], c2[2])
        for z1, z2 in z_exclusions:
            cubes.append([(minx, maxx), (miny, maxy), (z1, z2)])
        return cubes
    else:
        return [c2]

def range_size(p):
    return (p[1] - p[0]) + 1

def size(cube):
    total = 1
    for p in cube:
        total *= range_size(p)
    return total

with open("input") as f:
    input = f.read()

lines = [line.strip().split(" ") for line in input.strip().split("\n")]
cubes = [[l[0] == "on", [[int(y) for y in x.split("=")[1].split("..")] for x in l[1].split(",")]] for l in lines]


def calculate_cube_iter(init_index, init_cubes, init_default_turn_on):
    count = 0
    stack = [(init_index, init_cubes, init_default_turn_on)]
    while stack:
        index, cubes, default_turn_on = stack.pop(0)
        turn_on, cube = cubes[index]

        overlaps = []
        exclusions = []

        for i in range(index + 1, len(cubes)):
            other_turn_on, other_cube = cubes[i]
            overlap = get_overlap(cube, other_cube)
            if overlap is not None:
                overlaps.append([other_turn_on, overlap])
            exclusions += [[other_turn_on, ecube] for ecube in get_exclusion(cube, other_cube)]

        if exclusions:
            stack.append((0, exclusions, default_turn_on))

        if turn_on and not default_turn_on:
            count += size(cube)
        elif not turn_on and default_turn_on:
            count -= size(cube)

        if len(overlaps) > 0:
            stack.append((0, overlaps, turn_on))
    return count

size = calculate_cube_iter(0, cubes, False)
print(size)