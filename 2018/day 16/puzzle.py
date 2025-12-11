
with open("input") as f:
    first_part, second_part = f.read().strip().split("\n\n\n\n")
    parts = first_part.split("\n\n")
    instructions = [[int(x) for x in line.split(" ")] for line in second_part.split("\n")]

def swap(x, i, v):
    return tuple(v if j == i else y for j, y in enumerate(x))

commands = {
    "addr": lambda r, a, b, c: swap(r, c, r[a] + r[b]),
    "addi": lambda r, a, b, c: swap(r, c, r[a] + b),
    "mulr": lambda r, a, b, c: swap(r, c, r[a] * r[b]),
    "muli": lambda r, a, b, c: swap(r, c, r[a] * b),
    "banr": lambda r, a, b, c: swap(r, c, r[a] & r[b]),
    "bani": lambda r, a, b, c: swap(r, c, r[a] & b),
    "borr": lambda r, a, b, c: swap(r, c, r[a] | r[b]),
    "bori": lambda r, a, b, c: swap(r, c, r[a] | b),
    "setr": lambda r, a, b, c: swap(r, c, r[a]),
    "seti": lambda r, a, b, c: swap(r, c, a),
    "gtir": lambda r, a, b, c: swap(r, c, int(a > r[b])),
    "gtri": lambda r, a, b, c: swap(r, c, int(r[a] > b)),
    "gtrr": lambda r, a, b, c: swap(r, c, int(r[a] > r[b])),
    "eqir": lambda r, a, b, c: swap(r, c, int(a == r[b])),
    "eqri": lambda r, a, b, c: swap(r, c, int(r[a] == b)),
    "eqrr": lambda r, a, b, c: swap(r, c, int(r[a] == r[b])),
}

def find_possible_ops(sample):
    before, ins, after = sample
    vals = ins[1:]
    return [(name, ins[0]) for name, proc in commands.items() if proc(before, *vals) == after]

samples = []
for part in parts:
    before, instruction, after = part.strip().split("\n")
    before_registers = tuple([int(x.strip()) for x in before.split(":")[1].strip()[1:-1].split(",")])
    after_registers = tuple([int(x.strip()) for x in after.split(":")[1].strip()[1:-1].split(",")])
    instruction = tuple([int(x) for x in instruction.strip().split(" ")])
    samples.append((before_registers, instruction, after_registers))

opcode_possibilities = [set() for _ in range(len(commands))]
for s in samples:
    for name, code in find_possible_ops(s):
        opcode_possibilities[code].add(name)

opcode_map = [None] * len(commands)
opcodes_to_identify = list(range(len(commands)))
while opcodes_to_identify:
    remaining = []
    for code in opcodes_to_identify:
        if len(opcode_possibilities[code]) == 1:
            name = next(iter(opcode_possibilities[code]))
            opcode_map[code] = name
            for poss in opcode_possibilities:
                poss.discard(name)
        else:
            remaining.append(code)
    opcodes_to_identify = remaining

print(opcode_map)

registers = (0, 0, 0, 0)
for code, a, b, c in instructions:
    name = opcode_map[code]
    registers = commands[name](registers, a, b, c)
print(registers[0])

#for s in samples:
#    print(find_possible_ops(s))

#print(len([s for s in samples if len(find_possible_ops(s)) >= 3]))


