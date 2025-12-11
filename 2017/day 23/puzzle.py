from collections import defaultdict

def val(x, registers):
    if isinstance(x, int):
        return x
    else:
        return registers[x]
    
def try_int(x):
    try:
        return int(x)
    except:
        return x

def set(x, y):
    def cmd(registers):
        registers[x] = val(y, registers)
        return 1
    return cmd

def sub(x, y):
    def cmd(registers):
        if x == "h":
            bval = registers["b"]
            print(f"bval {bval} caused h to increment")
        registers[x] -= val(y, registers)
        return 1
    return cmd

def mul(x, y):
    def cmd(registers):
        registers[x] *= val(y, registers)
        return 1
    return cmd

def jump(x, y):
    def cmd(registers):
        if val(x, registers) != 0:
            return val(y, registers)
        return 1
    return cmd

registers = defaultdict(int)
registers["a"] = 1

instructions = []
with open("input") as f:
    for line in f.read().strip().split("\n"):
        cmd = line.split(" ")
        match cmd[0]:
            case "set": instructions.append(set(cmd[1], try_int(cmd[2])))
            case "sub": instructions.append(sub(cmd[1], try_int(cmd[2])))
            case "mul": instructions.append(mul(cmd[1], try_int(cmd[2])))
            case "jnz": instructions.append(jump(try_int(cmd[1]), try_int(cmd[2])))


pointer = 0
while 0 <= pointer < len(instructions):
#for _ in range(10_000):
    pointer += instructions[pointer](registers)

print(registers)

print(registers["h"])