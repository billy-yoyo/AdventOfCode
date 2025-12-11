import re
import functools

generator_regex = re.compile(r"([a-zA-Z]+) generator")
chip_regex = re.compile(r"([a-zA-Z]+)-compatible")

with open("input") as f:
    lines = f.read().strip().split("\n")
    floors = tuple([
        tuple(sorted([
            ("gen", name.group(1)) for name in generator_regex.finditer(line)
        ] + [
            ("chip", name.group(1)) for name in chip_regex.finditer(line)
        ])) for line in lines
    ])

def move(floors, items, from_floor, to_floor):
    return tuple(
        tuple(x for x in floor if x not in items) if i == from_floor else (
            tuple(sorted(floor + tuple(items))) if i == to_floor else floor
        ) for i, floor in enumerate(floors)
    )

def floor_is_valid(floor):
    gens = [x_name for x_type, x_name in floor if x_type == "gen"]
    chips = [x_name for x_type, x_name in floor if x_type == "chip"]

    if len(gens) == 0:
        return True
    elif len(chips) == 0:
        return True
    else:
        return all(chip in gens for chip in chips)

def try_move(floors, items, from_floor, to_floor):
    # a chip and gen of different types cannot be moved together
    #if any(item[0] == "gen" for item in items) and to_floor < from_floor:
    #    return None
    if len(items) == 2 and items[0][0] != items[1][0] and items[0][1] != items[1][1]:
        return None
    else:
        new_floors = move(floors, items, from_floor, to_floor)
        if not floor_is_valid(new_floors[from_floor]) or not floor_is_valid(new_floors[to_floor]):
            return None
        return new_floors

def maybe_add_to_stack(visited, next_stack, floors, items, from_floor, to_floor):
    move = try_move(floors, items, from_floor, to_floor)
    if move is not None and (to_floor, move) not in visited:
        next_stack.append((to_floor, move))

def bfs(initial_elevator, initial_floors):
    stack = [(initial_elevator, initial_floors)]
    visited = {}
    step = 0
    while stack:
        print(f"step {step}, stack has {len(stack)} items")
        next_stack = []
        for elevator, floors in stack:
            visited[(elevator, floors)] = True
            if all(len(x) == 0 for x in floors[:-1]):
                return step

            for i, item_1 in enumerate(floors[elevator]):
                if elevator > 0:
                    maybe_add_to_stack(visited, next_stack, floors, (item_1,), elevator, elevator - 1)

                if elevator < len(floors) - 1:
                    maybe_add_to_stack(visited, next_stack, floors, (item_1,), elevator, elevator + 1)
                
                for j in range(i):
                    item_2 = floors[elevator][j]
                    if elevator > 0:
                        maybe_add_to_stack(visited, next_stack, floors, (item_1, item_2), elevator, elevator - 1)

                    if elevator < len(floors) - 1:
                        maybe_add_to_stack(visited, next_stack, floors, (item_1, item_2), elevator, elevator + 1)
        step += 1
        stack = next_stack

print(floors)
print(bfs(0, floors))


