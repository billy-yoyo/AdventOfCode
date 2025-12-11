import functools

room_size = 4
hole_size = 2


initial_state = (
    "",
    "CDDD",
    "",
    "ABCB",
    "",
    "DABC",
    "",
    "BCAA",
    ""
)

def get_room(i):
    return (i * 2) + 1

def get_corridor(i):
    return (i + 1) * 2

def get_hole(i):
    return i * 8

def is_room(n):
    return n in (1, 3, 5, 7)

def is_hole(n):
    return n in (0, 8)

def is_corridor(n):
    return n in (2, 4, 6)

def get_room_type(i):
    return "ABCD"[(i - 1) // 2]

def path_length(state, start, end):
    length = 0

    # length to get out of the room or hole
    if is_room(start):
        length += room_size - len(state[start])
    elif is_hole(start):
        length += hole_size - len(state[start])
    
    # length to get into the room or hole
    if is_room(end):
        length += room_size - (len(state[end]) + 1)
    elif is_hole(end):
        length += hole_size - (len(state[end]) + 1)

    # length to move
    if is_room(start) and is_room(end):
        length += abs(start - end) + 2
    elif (is_room(start) and is_hole(end)) or (is_room(end) and is_hole(start)):
        room = start if is_room(start) else end
        hole = start if is_hole(start) else end
        if hole == 0:
            length += room + 1
        else:
            length += 9 - room
    elif (is_room(start) and is_corridor(end)) or (is_room(end) and is_corridor(start)):
        length += abs(start - end) + 1
    elif is_hole(start) and is_hole(end):
        length += 8
    elif (is_hole(start) and is_corridor(end)) or (is_hole(end) and is_corridor(start)):
        corridor = start if is_corridor(start) else end
        hole = start if is_hole(start) else end
        if hole == 0:
            length += corridor
        else:
            length += 8 - corridor
    elif is_corridor(start) and is_corridor(end):
        length += abs(start - end)

    return length

def path_clear(state, start, end):
    for i in range(min(start, end) + 1, max(start, end)):
        if is_corridor(i) and len(state[i]) > 0:
            return False
    return True

letter_costs = {
    "D": 1000,
    "C": 100,
    "B": 10,
    "A": 1
}

def path_cost(state, start, end):
    if len(state[start]) > 0:
        letter = state[start][-1]
        return letter_costs[letter] * path_length(state, start, end)
    else:
        return -1

def swap(state, start, end):
    return tuple(
        x[:-1] if i == start else (x + state[start][-1] if i == end else x) for i, x in enumerate(state)
    )

def can_move(state, start, end):
    if len(state[start]) > 0:
        letter = state[start][-1]
        end_len = len(state[end])

        # can't move from outside a room to outside a room
        if not is_room(start) and not is_room(end):
            return False
        # can't move into a room that doesn't match your letter
        elif is_room(end) and letter != get_room_type(end):
            return False
        # can't move into a room that matches your letter unless that room is empty or only contains correct letters
        elif is_room(end) and (end_len != 0 and set(state[end]) != {get_room_type(end)}):
            return False
        # can't move if there is anyone in a corridor between the start and end
        elif not path_clear(state, start, end):
            return False
        # can't move out of your room if your room is correct 
        elif is_room(start) and set(state[start]) == {get_room_type(start)}:
            return False
        # can't move ito a room, hole or corridor that's full
        elif (is_room(end) and end_len < room_size) or (is_hole(end) and end_len < hole_size) or end_len == 0:
            return True
        else:
            return False
    else:
        return False

def state_finished(state):
    for i in range(4):
        room = state[get_room(i)]
        room_letter = get_room_type(get_room(i))
        if len(room) < room_size or any(x != room_letter for x in room):
            return False
    return True

def get_valid_moves(state):
    for start in range(len(state)):
        if len(state[start]) > 0:
            for end in range(len(state)):
                if start != end:
                    new_cost = path_cost(state, start, end)
                    if new_cost >= 0 and can_move(state, start, end):
                        yield (start, end, new_cost)

@functools.cache
def cost_for_state(state):
    if state_finished(state):
        return 0

    best_cost = None
    for start, end, step_cost in get_valid_moves(state):
        new_cost = cost_for_state(swap(state, start, end))
        if new_cost is not None:
            total_cost = new_cost + step_cost
            if best_cost is None or total_cost < best_cost:
                best_cost = total_cost
    
    return best_cost

print(cost_for_state(initial_state))
