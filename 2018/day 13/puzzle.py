from collections import defaultdict

with open("input") as f:
    lines = f.read().split("\n")

width = max(len(line) for line in lines)
height = len(lines) 
graph = {}
gchar = {}

# (y, x, direction, rot_count)
carts = []

offsets = [
    (0, -1), (1, 0), (0, 1), (-1, 0)
]

def get_c(x, y):
    if 0 <= y < height and 0 <= x < len(lines[y]):
        return lines[y][x]
    return " "

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c in "-<>":
            gc = "-"
        elif c in "|^v":
            gc = "|"
        elif c == "/":
            gc = "/"
        elif c == "\\":
            gc = "\\"
        elif c == "+":
            gc = "+"
        else:
            if c != " ":
                print(f"missed c {c}")
            continue
        gchar[(x, y)] = gc

        if c in "<>v^":
            carts.append([y, x, "^>v<".index(c), 0])

def find_collision(carts):
    positions = {}
    carts.sort()
    carts = [[y, x, d, r, i] for i, (y, x, d, r) in enumerate(carts)]
    cart_is_dead = [False] * len(carts)
    living_carts = len(carts)
    for y, x, _, _, i in carts:
        positions[(x, y)] = i
    
    t = 0
    while living_carts > 1:
        t += 1
        for index, (y, x, direction, rot_count, i) in enumerate(carts):
            if cart_is_dead[i]:
                continue
            if (x, y) not in graph:
                print(f"cart {i=} {x=} {y=} {direction=} went off the graph ({lines[y][x]}, {lines[y][x - 1]})")
            if living_carts <= 3:
                print(f"cart {i=} {x=} {y=} {direction=}")
            gc = gchar[(x, y)]
            # intersections
            if gc == "+":
                new_direction = [
                    (direction - 1) % 4,
                    direction,
                    (direction + 1) % 4
                ][rot_count % 3]
                rot_count += 1
            elif gc == "-" and direction % 2 == 1:
                new_direction = direction
            elif gc == "|" and direction % 2 == 0:
                new_direction = direction
            elif gc == "/":
                new_direction = [1, 0, 3, 2][direction]
            elif gc == "\\":
                new_direction = [3, 2, 1, 0][direction]
            ox, oy = offsets[new_direction]
            nx, ny = x + ox, y + oy
            if (x, y) in positions:
                del positions[(x, y)]
            else:
                print(f"cart {i=} {x=} {y=} {direction=} had a missing position on tick {t=}")
            if (nx, ny) in positions:
                other_i = positions[(nx, ny)]
                print(f"cart {i} and {other_i} crashed at {nx},{ny}")
                cart_is_dead[other_i] = True
                cart_is_dead[i] = True
                living_carts -= 2
                del positions[(nx, ny)]
            else:
                positions[(nx, ny)] = i
                carts[index] = [ny, nx, new_direction, rot_count, i]
        carts.sort()
    
    return next(((x, y) for y, x, _, _, i in carts if not cart_is_dead[i]))

print(find_collision(carts))

        
