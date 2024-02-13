import math
from functools import cache

#total_players, total_marbles = 476, 71431
total_players, total_marbles = 10, 1618
#total_players, total_marbles = 9, 25

def calc(max_marbles):
    wins = []
    scores = [0] * total_players
    stack = [0, 1]
    pointer = 1
    for marble in range(2, max_marbles + 1):
        player = (marble - 1) % total_players
        if marble % 23 == 0:
            removed = (pointer - 7) % len(stack)
            removed_score = stack.pop(removed)
            print(f"player {player} for {removed_score}")
            scores[player] += marble + removed_score
            wins.append((player, marble, removed_score))
            pointer = removed
        else:
            pointer = (pointer + 2) % len(stack)
            stack.insert(pointer, marble)
    return stack, wins

@cache
def two_series(n):
    x = 0
    p = 2
    while n > x:
        x += p
        p *= 2
    return (x // 2) + 1

@cache
def lazy_index(entry):
    if entry == 0:
        return 0, 1
    elif entry == 1:
        return 1, 2
    else:
        last_index, elements = lazy_index(entry - 1)
        if entry % 23 == 0:
            return (last_index - 7) % elements, elements - 1
        else:
            index = (last_index + 2) % (elements + 1)
            if index == 0:
                return index + 1, elements + 1
            else:
                return index, elements + 1

def get_entry_index(entry):
    return lazy_index(entry)[0]

def unshifted_entry_index(entry):
    if entry == 0:
        return 0
    elif entry == 1:
        return 1
    else:
        x = two_series(entry)
        return 1 + ((entry - x) * 2)

    
def shifted_entry(entry):
    unshifted = unshifted_entry_index(entry)
    unshifted -= 9 * (entry // 23)
    return unshifted % (entry + 1 - (2 * (entry // 23)))

cached_cell_values = {}

def cell_value(index, entry):
    initial_entry = entry
    entry_bound, entry_bound_value = 0, 0
    if index in cached_cell_values:
        entry_bound, entry_bound_value = cached_cell_values[index]

    if index >= entry + 1:
        return None
    
    entry_index = get_entry_index(entry)
    if index == entry_index and entry % 23 != 0:
        cached_cell_values[index] = (entry, entry)
        return entry
    
    while entry > entry_bound and (index != entry_index or entry % 23 == 0):
        if entry % 23 == 0:
            if entry_index <= index:
                index += 1
        elif entry_index <= index:
            index -= 1
        entry -= 1
        entry_index = get_entry_index(entry)

    if entry == entry_bound:
        entry = entry_bound_value

    cached_cell_values[index] = (initial_entry, entry)
    return entry

def fast_calc():
    #wins_iter = iter(calc(total_marbles)[1])

    scores = [0] * total_players
    for i in range(23, total_marbles + 1, 23):
        index = get_entry_index(i)
        removed_value = cell_value(index, i - 1)
        player = (i - 1) % total_players
        #print(f"[quick] player {player} wins {removed_value} + {i} on marble {i}")
        #real_p, real_marble, real_removed = next(wins_iter)
        #print(f"[ slow] player {real_p} wins {real_removed} + {real_marble} on marble {real_marble}")
        scores[player] += i + removed_value

    print(max(scores))

def dyn_pro():
    grid = [None] * total_marbles
    for i in range(total_marbles):
        grid[i] = [None] * total_marbles
    



#for i in range(44, 48):
#    stack, _ = calc(i)
#    zero_index = stack.index(0)
#    stack = stack[zero_index:] + stack[:zero_index] 
#    print(f"# {i} {shifted_entry(i)} {cell_value(shifted_entry(i), i)}")
#    print(" ".join(str(x) for x in stack))

#for i in range(total_marbles):
#    get_entry_index(i)

#fast_calc()
calc(total_marbles)
#print(f"computed with {cache_hits[0]} cache hits")

#print(" ".join(str(two_series(i - 1)) for i in range(15)))


#print(max(scores))

