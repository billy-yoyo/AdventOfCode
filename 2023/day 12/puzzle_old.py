import functools


def combinations_gen(sizes, total):
    min_size = sum(sizes) + len(sizes) - 1
    if min_size > total:
        return
    if len(sizes) == 0:
        yield 1
    elif len(sizes) == 1:
        yield 1 + total - sizes[0]
    else:
        for i in range(total - sizes[0]):
            yield from combinations_gen(sizes[1:], total - (sizes[0] + i + 1))

@functools.cache
def combinations(sizes, total):
    if len(sizes) == 0:
        return 1
    elif total < 0:
        return 0
    return sum(combinations_gen(sizes, total))

def gen_sections(sections, index, stack, stack_index, current):
    next_group_size = 0
    if stack_index < len(stack):
        next_group_size = stack[stack_index]

    while index < len(sections):
        section_char, section_size = sections[index]
        index += 1
        if section_char == "#":
            current += section_size
            if current > next_group_size:
                return 0
        elif section_char == ".":
            if current > 0 and current == next_group_size:
                stack_index += 1
                if stack_index < len(stack):
                    next_group_size = stack[stack_index]
                else:
                    next_group_size = 0
                current = 0
            elif current > 0 and current != next_group_size:
                return 0
        elif section_char == "?":
            if current > 0:
                # all ? as # and consume group
                if section_size + current <= next_group_size:
                    current += section_size
                    continue
                elif section_size + current == next_group_size + 1:
                    # first x as #, and one more as a .
                    stack_index += 1
                    if stack_index < len(stack):
                        next_group_size = stack[stack_index]
                    else:
                        next_group_size = 0
                    current = 0
                    continue
                else:
                    # first x as #, and one more as a .
                    section_size -= 1 + next_group_size - current
                    stack_index += 1
                    if stack_index < len(stack):
                        next_group_size = stack[stack_index]
                    else:
                        next_group_size = 0
                    current = 0

            # all ? as .
            if next_group_size == 0:
                continue

            # this is the final group, we can just count groups
            if index == len(sections):
                return combinations(tuple(stack[stack_index:]), section_size)
                
            # assume all .
            total = gen_sections(sections, index, stack, stack_index, 0)

            for i in range(stack_index+1, len(stack)+1):
                min_size = sum(stack[stack_index:i-1]) + len(stack[stack_index:i-1]) - 1
                if min_size > section_size:
                    break
                sub_stack = stack[stack_index:i]

                everything_combo = combinations(tuple(sub_stack), section_size - 1)
                if everything_combo > 0:
                    total += everything_combo * gen_sections(sections, index, stack, i, 0)

                for last_item_size in range(1, min(section_size, sub_stack[-1]) + 1):
                    combos = combinations(tuple(sub_stack[:-1]), section_size - (last_item_size + 1))
                    if combos > 0:
                        solns = gen_sections(sections, index, stack, i - 1, last_item_size)
                        total += combos * solns
            

            return total
    
    if stack_index == len(stack) or (stack_index == len(stack) - 1 and current == stack[-1]):
        return 1
    else:
        return 0

def get_by_section(line, stack):
    sections = []
    last = None
    start = 0
    for x, c in enumerate(line):
        if last is None:
            last = c
        elif last != c:
            sections.append((last, x - start))
            start = x
            last = c
    sections.append((last, len(line) - start))

    return gen_sections(sections, 0, stack, 0, 0)

with open("example") as f:
    total = 0
    total_5 = 0
    for i, line in enumerate(f):
        left, right = line.strip().split(" ")
        left_5 = "".join([left + "?"] * 4) + left
        stack = [int(x) for x in right.split(",")]
        total += get_by_section(left, stack)
        total_5 += get_by_section(left_5 + ".", stack * 5)
    print(total)
    print(total_5)
