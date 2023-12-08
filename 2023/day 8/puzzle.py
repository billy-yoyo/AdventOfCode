import math

with open("input") as f:
    top_line, rest = f.read().strip().split("\n\n")
    rest = { x.strip() : (y.strip()[1:-1].split(", ")) for x, y in [l.split(" = ") for l in rest.strip().split("\n")] }

instructions = top_line.strip()
current_stack = [x for x in rest.keys() if x.endswith("A")]
initial_stack = list(current_stack)
z_indexes = [[] for x in current_stack]
index = 0
while index < 100000:
    ins = instructions[index % len(instructions)]
    for i in range(len(current_stack)):
        if current_stack[i] is None:
            continue

        next_tuple = rest[current_stack[i]]
        if ins == "R":
            current_stack[i] = next_tuple[1]
        else:
            current_stack[i] = next_tuple[0]
    
        if current_stack[i].endswith("Z"):
            z_indexes[i].append(index)
        elif current_stack[i] == initial_stack[i] and index % 2 == 0:
            current_stack[i] = None
        
    index += 1

periods = [l[1] - l[0] for l in z_indexes]
answer = 1
for period in periods:
    answer = math.lcm(answer, period)
print(answer)

