from collections import defaultdict

with open("input") as f:
    instructions = [x.split(" ") for x in f.read().strip().split("\n")]

registers = defaultdict(int)

def val(x):
    try:
        return int(x)
    except:
        return registers[x]

registers["c"] = 1

steps = 0
pointer = 0
while pointer < len(instructions):
    ins = instructions[pointer]
    if ins[0] == "cpy":
        _, value, destination = ins
        registers[destination] = val(value)
    elif ins[0] == "inc":
        _, destination = ins
        registers[destination] += 1
    elif ins[0] == "dec":
        _, destination = ins
        registers[destination] -= 1
    elif ins[0] == "jnz":
        _, condition, offset = ins
        if val(condition) != 0:
            pointer += val(offset)
            continue
    else:
        raise Exception(f"invalid ins: {ins}")
    pointer += 1

print(registers["a"])
