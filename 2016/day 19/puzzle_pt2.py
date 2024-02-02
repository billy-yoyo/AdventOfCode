
# 1 2 3 4 5
# 1 2 . 4 5
# 1 2 . 4 .
# . 2 . 4 .
# . 2 . . .

total_count = 3018458
#total_count = 5

elves = list(range(1, total_count + 1))
size = len(elves)

next_elf = list(elves)
prev_elf = [(i - 1) % size for i in range(total_count)]
next_elf[-1] = 0

remaining = len(elves)

def remove(x):
    elves[x] = None
    pi = prev_elf[x]
    ni = next_elf[x]
    next_elf[pi] = ni
    prev_elf[ni] = pi

def step_by(start, count):
    index = start
    for _ in range(count):
        index = next_elf[index]
    return index

index = 0
opposite_index = step_by(index, remaining // 2)
is_odd = total_count % 2 == 0
while remaining > 1:
    remove(opposite_index)
    remaining -= 1
    index = step_by(index, 1)
    opposite_index = step_by(opposite_index, 1 if is_odd else 2)
    is_odd = not is_odd


print(next(x for x in elves if x is not None))
