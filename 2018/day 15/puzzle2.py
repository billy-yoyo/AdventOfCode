from collections import defaultdict, deque
import math

grid = defaultdict(int)
units = {}
killed = set()

GROUND = 0
WALL = 1
ELF = 2
GOBLIN = 3

TYPE_MAP = ".#EG"

offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

class Unit:
    def __init__(self, x, y, type, uid, ap=3):
        self.x = x
        self.y = y
        self.type = type
        self.target_type = ELF if type == GOBLIN else GOBLIN
        self.uid = uid
        self.hp = 200
        self.ap = ap

        self.died = False
        self.attacked = False
        self.moved = False
        self.turn_damage = 0

    def reset_turn(self):
        self.died = False
        self.attacked = False
        self.moved = False
        self.turn_damage = 0

    def surrounded(self):
        return all(grid[(self.x + ox, self.y + oy)] != GROUND for ox, oy in offsets)

    def get_move_destination(self):
        targets = [(u.x, u.y) for u in units.values() if u.type == self.target_type and not u.surrounded()]
        if len(targets) == 0:
            return None
        
        stack = deque([(None, (self.x, self.y), 0)])
        visited = set()
        found = []
        found_at = None
        while stack:
            path_start, (sx, sy), steps = stack.popleft()
            if found_at is not None and steps > found_at:
                continue
            
            for ox, oy in offsets:
                npos = sx + ox, sy + oy
                grid_type = grid[npos]
                if grid_type == self.target_type:
                    if path_start is None:
                        return None
                    elif found_at is None or steps < found_at:
                        found = [(sy, sx, path_start[1], path_start[0])]
                        found_at = steps
                    elif steps == found_at:
                        found.append((sy, sx, path_start[1], path_start[0]))
                elif grid_type == GROUND:
                    if npos in visited:
                        continue
                    visited.add(npos)
                    stack.append((npos if path_start is None else path_start, npos, steps + 1))
        if len(found) == 0:
            return None
        _, _, ty, tx = min(found)
        return tx, ty

    def move(self):
        dest = self.get_move_destination()
        if dest is not None:
            nx, ny = dest
            grid[(self.x, self.y)] = GROUND
            self.x = nx
            self.y = ny
            grid[(self.x, self.y)] = self.type
            return True
        return False

    def attack(self):
        neighbours = [((unit.hp, unit.y, unit.x), unit) for unit in units.values() if unit.type == self.target_type and abs(self.x - unit.x) + abs(self.y - unit.y) == 1]
        if len(neighbours) > 0:
            _, unit = min(neighbours, key=lambda x: x[0])
            self.attacked = True
            if unit.hp <= self.ap:
                unit.died = True
                del units[unit.uid]
                grid[(unit.x, unit.y)] = GROUND
                if len(set(u.type for u in units.values())) == 1:
                    return True
            else:
                unit.hp -= self.ap
                unit.turn_damage += self.ap
        else:
            self.attacked = False

    def do_turn(self):
        if self.died:
            return False
        if self.move():
            self.moved = True
        return self.attack()

def print_grid():
    print("\n".join([
        "".join(
            TYPE_MAP[grid[(x, y)]] for x in range(width)
        )
        for y in range(height)
    ]))

def run_game():
    rounds = 0
    while True:
        #print(f"round {rounds}:")
        #print(", ".join(f"{TYPE_MAP[u.type]}({u.uid}, {u.hp})" for u in units.values()))
        #print_grid()

        turn_order = sorted([((u.y, u.x), u.uid) for u in units.values()], key=lambda x: x[0])
        
        for unit in units.values():
            unit.reset_turn()
        
        for index, (_, uid) in enumerate(turn_order):
            if uid not in units:
                continue
            if units[uid].do_turn():
                return rounds + (index == len(turn_order) - 1)
        
        rounds += 1
        # if nobody moved, and nobody died, we can skip into the future a bit
        if all(not unit.moved for unit in units.values()) and len(turn_order) == len(units):
            turns_to_dead = min(math.ceil(unit.hp / unit.turn_damage) for unit in units.values() if unit.turn_damage > 0)
            if turns_to_dead > 1:
                skip_turns = turns_to_dead - 1
                rounds += skip_turns
                for unit in units.values():
                    unit.hp -= unit.turn_damage * skip_turns

# part 1


# part 2
elf_ap = 4
while True:
    grid.clear()
    units.clear()
    killed.clear()

    with open("input") as f:
        unit_id = 0
        for y, line in enumerate(f.read().strip().split("\n")):
            for x, c in enumerate(line):
                grid[(x, y)] = TYPE_MAP.index(c)
                if c == "G":
                    unit_id += 1
                    units[unit_id] = Unit(x, y, GOBLIN, unit_id)
                elif c == "E":
                    unit_id += 1
                    units[unit_id] = Unit(x, y, ELF, unit_id, elf_ap)


    width = max(x for x, _ in grid.keys()) + 1
    height = max(y for _, y in grid.keys()) + 1
    total_elves = len([u for u in units.values() if u.type == ELF])

    rounds = run_game()
    total_hp = sum(u.hp for u in units.values())
    surviving_elves = len([u for u in units.values() if u.type == ELF])
    print(f"{rounds=} {total_hp=}")
    print(rounds * total_hp)

    if surviving_elves == total_elves:
        print(f"success with ap {elf_ap}")
        break
    elf_ap += 1
        
