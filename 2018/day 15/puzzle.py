from collections import defaultdict

grid = defaultdict(int)
units = []
killed = set()

GROUND = 0
WALL = 1
ELF = 2
GOBLIN = 3

TYPE_MAP = ".#EG"

with open("input") as f:
    unit_id = 0
    for y, line in enumerate(f.read().strip().split("\n")):
        for x, c in enumerate(line):
            grid[(x, y)] = TYPE_MAP.index(c)
            if c == "G":
                unit_id += 1
                units.append((y, x, 200, 3, GOBLIN, unit_id))
            elif c == "E":
                unit_id += 1
                units.append((y, x, 200, 3, ELF, unit_id))

width = max(x for x, _ in grid.keys()) + 1
height = max(y for _, y in grid.keys()) + 1

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def choose_move(x, y, ap, unit_type):
    target_type = GOBLIN if unit_type == ELF else ELF
    targets = sum(1 for _, _, _, _, t, _ in units if t == target_type)
    if targets == 0:
        return (x, y), True, None

    # move
    stack = [[(x, y)]]
    found = []
    while stack and not found:
        next_stack = []
        for path in stack:
            sx, sy = path[-1]
            for ox, oy in offsets:
                nx, ny = sx + ox, sy + oy
                if (nx, ny) in path:
                    continue
                grid_type = grid[(nx, ny)]
                if grid_type == target_type:
                    found.append(path)
                elif grid_type == GROUND:
                    next_stack.append(path + [(nx, ny)])
        stack = next_stack

    if len(found) == 0:
        return (x, y), False, None
    
    # if we're already next to a target we will have found a single path, with length 1
    if all(len(p) > 1 for p in found):
        ty, tx = min(path[-1][::-1] for path in found)
        ny, nx = min(path[1][::-1] for path in found if path[-1] == (tx, ty))
    else:
        nx, ny = x, y

    neighbours = [(hp, tx, ty, ap, i, uid) for i, (ty, tx, hp, ap, t, uid) in enumerate(units) if t == target_type and abs(tx - nx) + abs(ty - ny) == 1]
    # attack
    attack = None
    if len(neighbours) > 0:
        neighbours.sort()
        hp, tx, ty, tap, i, uid = neighbours[0]
        attack = (uid, ap)
        #print(f"{x},{y} attacked {tx},{ty}")
        if hp <= ap:
            killed.add(uid)
            units.pop(i)
            grid[(tx, ty)] = GROUND
        else:
            units[i] = (ty, tx, hp - ap, tap, target_type, uid)

    return (nx, ny), False, attack

def turn():
    units.sort()
    turn_order = [uid for _, _, _, _, _, uid in units]
    for uid in turn_order:
        if uid in killed:
            continue
        y, x, hp, ap, unit_type, _ = next(unit for unit in units if unit[5] == uid)
        (nx, ny), finished, attack = choose_move(x, y, ap, unit_type)
        if finished:
            return True, 1
        #print(f"unit {i} moved from {x},{y} to {nx},{ny}")
        grid[(x, y)] = GROUND
        grid[(nx, ny)] = unit_type
        unit_index = next(i for i, unit in enumerate(units) if unit[5] == uid)
        units[unit_index] = (ny, nx, hp, ap, unit_type, uid)
    return False, 1

def play_game():
    
    round = 0
    while not turn():
        round += 1
    return round

def print_grid():
    print("\n".join([
        "".join(
            TYPE_MAP[grid[(x, y)]] for x in range(width)
        )
        for y in range(height)
    ]))

"""
for _ in range(3):
    print(units)
    print_grid()
    print()
    turn()

print(units)
print_grid()
"""

rounds = play_game()
final_hp = sum(hp for _, _, hp, _, _, _ in units)

print(f"{rounds=} {final_hp=}")
print(rounds * final_hp)