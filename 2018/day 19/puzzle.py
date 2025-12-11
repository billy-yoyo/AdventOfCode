
def swap(x, i, v):
    x[i] = v
    #return tuple(v if j == i else y for j, y in enumerate(x))

commands = {
    "addr": lambda a, b, c: lambda r: swap(r, c, r[a] + r[b]),
    "addi": lambda a, b, c: lambda r: swap(r, c, r[a] + b),
    "mulr": lambda a, b, c: lambda r: swap(r, c, r[a] * r[b]),
    "muli": lambda a, b, c: lambda r: swap(r, c, r[a] * b),
    "banr": lambda a, b, c: lambda r: swap(r, c, r[a] & r[b]),
    "bani": lambda a, b, c: lambda r: swap(r, c, r[a] & b),
    "borr": lambda a, b, c: lambda r: swap(r, c, r[a] | r[b]),
    "bori": lambda a, b, c: lambda r: swap(r, c, r[a] | b),
    "setr": lambda a, b, c: lambda r: swap(r, c, r[a]),
    "seti": lambda a, b, c: lambda r: swap(r, c, a),
    "gtir": lambda a, b, c: lambda r: swap(r, c, int(a > r[b])),
    "gtri": lambda a, b, c: lambda r: swap(r, c, int(r[a] > b)),
    "gtrr": lambda a, b, c: lambda r: swap(r, c, int(r[a] > r[b])),
    "eqir": lambda a, b, c: lambda r: swap(r, c, int(a == r[b])),
    "eqri": lambda a, b, c: lambda r: swap(r, c, int(r[a] == b)),
    "eqrr": lambda a, b, c: lambda r: swap(r, c, int(r[a] == r[b])),
}

registers = [0] * 6
ip = 0

instructions = []
with open("input") as f:
    for line in f.read().strip().split("\n"):
        if line.startswith("#"):
            ip = int(line[4:])
        else:
            name, a, b, c = line.strip().split(" ")
            instructions.append(commands[name](int(a), int(b), int(c)))

registers[0] = 1
while 0 <= registers[ip] < len(instructions):
    if registers[ip] == 1:
        print(registers)
    instructions[registers[ip]](registers)
    registers[ip] += 1

print(registers[0])
