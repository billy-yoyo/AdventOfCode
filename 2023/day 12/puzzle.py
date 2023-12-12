
def dyn_approach(line, stack):
    line_size, stack_size = len(line), len(stack)

    # dynamic function, with the following fields:
    #   position: the current index on 'line'
    #   groups_read: the number of groups we've read so far
    #   last_group: the length of the latest group we've been reading
    f = [[[0 for _ in range(line_size + 2)] for _ in range(stack_size + 2)] for _ in range (line_size + 1)]
    
    # add a group that definitely cannot complete to the end of the stack to make final-state checking simpler
    stack = stack + [line_size + 1]

    # initialize at position 0, with 0 groups read and current group size as 0
    f[0][0][0] = 1
    for position in range(line_size):
        for groups_read in range(stack_size + 1):
            for last_group in range(line_size + 1):
                # this is the number of configurations which can reach this state
                count = f[position][groups_read][last_group]
                if not count:
                    # don't bother continuing if we never reach here anyway
                    continue

                next_char = line[position]

                if next_char in ".?":
                    # we move forwards only if one of these conditions is met:
                    #   1. the last group is 0, and so we're not currently reading a group
                    #   2. the last group is exactly the same size as the appropraite group in the stack, so we can move on to a new group (eventually)
                    if last_group == 0 or last_group == stack[groups_read - 1]:
                        f[position + 1][groups_read][0] += count
                
                if next_char in "#?":
                    # we move forwards, increasing the final group size by 1, and startnig a new group if the existing final group size is 0.
                    f[position + 1][groups_read + (not last_group)][last_group + 1] += count
    
    # we read the number of configurations that managed to reach a state with all positions read, all groups read, and a final group size of 0.
    return f[line_size][stack_size][0]


with open("example") as f:
    total = 0
    total_5 = 0
    for i, line in enumerate(f):
        left, right = line.strip().split(" ")
        left_5 = "".join([left + "?"] * 4) + left
        stack = [int(x) for x in right.split(",")]
        total += dyn_approach(left, stack)
        total_5 += dyn_approach(left_5 + ".", stack * 5)
    print(total)
    print(total_5)

