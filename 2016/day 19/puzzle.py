

total_elves = 3018458
#total_elves = 5

def game_1():
    elves = [True] * total_elves

    count = 0

    i = 0
    while count < total_elves - 1:
        i = (i + 1) % total_elves
        while not elves[i]:
            i = (i + 1) % total_elves
        elves[i] = False
        while not elves[i]:
            i = (i + 1) % total_elves
        count += 1

    final_elf = elves.index(True)
    return final_elf + 1

def game_2():
    elves = [True] * total_elves
    remaining = total_elves

    i = 0
    while remaining > 1:
        to_skip = remaining // 2
        j = (i + 1) % total_elves
        while to_skip > 0:
            if elves[j]:
                to_skip -= 1
            j = (j + 1) % total_elves
        j = (j - 1) % total_elves
        elves[j] = False
        remaining -= 1

        i = (i + 1) % total_elves
        while not elves[i]:
            i = (i + 1) % total_elves
     
    final_elf = elves.index(True)
    return final_elf + 1

print(game_2())
