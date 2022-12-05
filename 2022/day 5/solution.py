
data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

with open("puzzle") as f:
    data = f.read()

data_first, data_last = data.split("\n\n")

initial_lines = data_first.split("\n")[:-1]
rows = [[line[i:i+4].strip() for i in range(0, len(line), 4)] for line in initial_lines]
columns = len(rows[-1])

stacks = [[] for x in range(columns)]

for row in reversed(rows):
    for x, value in enumerate(row):
        if value:
            stacks[x].append(value[1])

def read_instruction(line):
    move, positions = line.split(" from ")
    move_number = int(move[5:])
    positions = [int(x)-1 for x in positions.split(" to ")]
    return [move_number, *positions]

instructions = [read_instruction(line) for line in data_last.split("\n")]

for move, start, end in instructions:
    #for i in range(move):
    #    if stacks[start]:
    #        top = stacks[start].pop()
    #        stacks[end].append(top)

    top = stacks[start][-move:]
    stacks[start] = stacks[start][:-move]
    stacks[end] += top

code = "".join(stack[-1] for stack in stacks)
print(code)


