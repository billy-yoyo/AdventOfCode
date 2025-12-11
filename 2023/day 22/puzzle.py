from collections import defaultdict

cubes = []

with open("input") as f:
    for line in f.read().strip().split("\n"):
        left, right = [[int(x) for x in l.split(",")] for l in line.split("~")]
        cubes.append([
            [min(left[i], right[i]) for i in range(3)],
            [max(left[i], right[i]) for i in range(3)]
        ])

def collision_xy(left_cube, right_cube):
    lx0, ly0, lx1, ly1 = left_cube[0][0], left_cube[0][1], left_cube[1][0], left_cube[1][1]
    rx0, ry0, rx1, ry1 = right_cube[0][0], right_cube[0][1], right_cube[1][0], right_cube[1][1]

    return lx1 >= rx0 and lx0 <= rx1 and ly1 >= ry0 and ly0 <= ry1

z_layers = defaultdict(list)

cubes = sorted(cubes, key=lambda x: x[0][2])
cube_is_supporting = [list() for _ in cubes]
cube_is_supported_by = [list() for _ in cubes]

highest_z = 1

for i, cube in enumerate(cubes):
    layer = highest_z
    while layer > 0 and not any(collision_xy(cubes[cube_index], cube) for cube_index in z_layers[layer]):
        layer -= 1


    # what is this sitting on?
    
    for cube_index in z_layers[layer]:
        if collision_xy(cubes[cube_index], cube):
            cube_is_supporting[cube_index].append(i)
            cube_is_supported_by[i].append(cube_index)

    z_layers[layer + 1].append(i)
    highest_z = max(highest_z, layer + 1)

    if cube[0][2] != cube[1][2]:
        for offz in range(cube[1][2] - cube[0][2]):
            z_layers[layer + 2 + offz].append(i)
            highest_z = max(highest_z, layer + 2 + offz)
    
count = 0
falling_count = 0
for i in range(len(cubes)):
    if len(cube_is_supporting[i]) == 0:
        count += 1
    elif all(len(cube_is_supported_by[oi]) > 1 for oi in cube_is_supporting[i]):
        count += 1
    # this is a vulnerable brick
    else:
        affected = {i}
        stack = [x for x in cube_is_supporting[i] if all(y in affected for y in cube_is_supported_by[x])]
        while stack:
            next_stack = []
            for j in stack:
                affected |= {j}
                falling_count += 1
                next_stack += [x for x in cube_is_supporting[j] if all(y in affected for y in cube_is_supported_by[x])]
            stack = next_stack


#print(cube_is_supporting)
#print(cube_is_supported_by)
print(count)
print(falling_count)