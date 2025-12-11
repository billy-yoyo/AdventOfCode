import sys
import functools

room_size = 2
hole_size = 2

# state is
# (
# 0: left_hole, 
# 1: room_1,
# 2: corridor_1,
# 3: room_2, 
# 4: corridor_2,
# 5: room_3,
# 6: corridor_3,
# 7: room_4,
# 8: right_hole
# )

#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########

initial_state = (
    "",
    "CD",
    "",
    "AB",
    "",
    "DC",
    "",
    "BA",
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

def test():
    assert path_length(initial_state, get_room(0), get_hole(1)) == 9
    assert path_length(initial_state, get_room(0), get_hole(0)) == 3
    assert path_length(initial_state, get_room(0), get_corridor(0)) == 2
    assert path_length(initial_state, get_room(0), get_corridor(1)) == 4
    assert path_length(initial_state, get_room(0), get_corridor(2)) == 6
    assert path_length(initial_state, get_room(0), get_room(1)) == 4
    assert path_length(initial_state, get_room(0), get_room(3)) == 8
    assert path_length(initial_state, get_room(1), get_corridor(0)) == 3
    assert path_length(initial_state, get_room(1), get_hole(0)) == 6



cache = {}
visited = {}
current_lowest = [0]

#@functools.cache
def get_valid_moves(state):
    for start in range(len(state)):
        if len(state[start]) > 0:
            for end in range(len(state)):
                if start != end:
                    new_cost = path_cost(state, start, end)
                    if new_cost >= 0 and can_move(state, start, end):
                        yield (start, end, new_cost)


def pad(s, n):
    return s + "." * (n - len(s))

def cordot(s, i):
    if i < len(s):
        return s[i]
    else:
        return "."

def print_state(state):
    print(f"#############")
    print(f"#{pad(state[0], 2)}.{pad(state[2], 1)}.{pad(state[4], 1)}.{pad(state[6], 1)}.{pad(state[8], 2)[::-1]}#")
    print(f"###{cordot(state[1], 1)}#{cordot(state[3], 1)}#{cordot(state[5], 1)}#{cordot(state[7], 1)}###")
    print(f"  #{cordot(state[1], 0)}#{cordot(state[3], 0)}#{cordot(state[5], 0)}#{cordot(state[7], 0)}#")
    print("  ########")

def playout(initial_state, movement_stack):
    print_state(initial_state)
    state = initial_state
    for index, start, end, cost in movement_stack:
        state = swap(state, start, end)
        print("\n")
        print_state(state)

def playout_with_checks(initial_state, movement_stack):
    print_state(initial_state)
    state = initial_state
    total_cost = 0
    for index, start, end, cost in movement_stack:
        print("\n")
        real_cost = path_cost(state, start, end)
        if not can_move(state, start, end):
            print(f"state move invalid!")
            return
        else:
            state = swap(state, start, end)
        total_cost += real_cost
        #state = swap(state, start, end)
        print(f"cost: {real_cost}")
        print_state(state)
    print(f"\ntotal cost: {total_cost}")


def state_search(initial_state, starting_index=0, index_step=1, upper_bound=-1):
    visited = set()
    state = initial_state
    min_cost = upper_bound
    best_path = None
    total_cost = 0
    movement_stack = []
    index = starting_index
    while True:
        #movement_seq = tuple((start, end) for _, start, end, _ in movement_stack)
        #if movement_seq_target[:len(movement_seq)] == movement_seq:
        #    print(f"{movement_seq} :: {index} <------")
        #else:
        #    print(f"{movement_seq} :: {index}")

        #if state == initial_state:
        #    print(f"returned to start")

        #print(state)
        valid_moves = sorted([x for x in get_valid_moves(state)], key=lambda d: d[2])
        finished = state_finished(state)

        # no valid moves, roll back state
        if state in visited or len(valid_moves) <= index or finished or (min_cost >= 0 and total_cost >= min_cost):
            if not finished and len(movement_stack) == 0:
                break
            else:
                if finished:
                    if min_cost < 0 or total_cost < min_cost:
                        discount = compute_hole_discount(movement_stack)
                        print(f"found finish: {total_cost - discount}")
                        #playout(initial_state, movement_stack)
                        min_cost = total_cost
                        best_path = list(movement_stack)

                #print("no valid moves, rolling back movement")
                index, start, end, cost = movement_stack.pop()
                state = swap(state, end, start)
                total_cost -= cost
                if not movement_stack:
                    index += index_step
                else:
                    index += 1
        else:
            visited |= {state}
            if not movement_stack:
                print(f"{index} of {len(valid_moves)}")
            start, end, cost = valid_moves[index]
            if min_cost >= 0 and cost + total_cost >= min_cost:
                if not movement_stack:
                    index += index_step
                else:
                    index += 1
            else:
                movement_stack.append((index, start, end, cost))
                total_cost += cost
                state = swap(state, start, end)
                index = 0
    return min_cost, best_path

def compute_hole_discount(movement_stack):
    discount = 0
    sizes = [(0, False)] * 9
    for _, start, end, _ in movement_stack:
        if is_hole(end):
            size, _ = sizes[end]
            if size >= 1:
                sizes[end] = (size + 1, True)
            else:
                sizes[end] = (1, False)
        
        if is_hole(start):
            size, has_been_full = sizes[start]
            if size == 1:
                if not has_been_full:
                    discount += 2
                sizes[start] = (0, False)
            else:
                sizes[start] = (size - 1, has_been_full)
    return discount


#for start, end, new_cost, new_state in get_valid_moves(initial_state):
#    print(f"{start}->{end} : {new_cost} : {new_state}")

#print(get_min_cost_for_state(initial_state))


movement_stack = [
    (0, get_room(2), get_corridor(0), 0),
    (0, get_room(1), get_room(2), 0),
    (0, get_room(1), get_corridor(1), 0),
    (0, get_corridor(0), get_room(1), 0),
    (0, get_room(0), get_room(1), 0),
    (0, get_room(3), get_corridor(2), 0),
    (0, get_room(3), get_hole(1), 0),
    (0, get_corridor(2), get_room(3), 0),
    (0, get_corridor(1), get_room(3), 0),
    (0, get_hole(1), get_room(0), 0),
]

#print(compute_hole_discount(movement_stack))

movement_seq_target = tuple((start, end) for _, start, end, _ in movement_stack)
#print(movement_seq_target)

#print(movement_stack)
starting_index = int(sys.argv[1])
index_step = int(sys.argv[2])
upper_bound = int(sys.argv[3])
min_cost, best_path = state_search(initial_state, starting_index=starting_index, index_step=index_step, upper_bound=upper_bound)
min_cost -= compute_hole_discount(best_path)
print(min_cost)
#print()

#playout_with_checks(initial_state, movement_stack)
