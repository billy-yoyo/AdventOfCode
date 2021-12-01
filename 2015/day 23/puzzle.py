
registers = { "a": 1, "b": 0 }
def set(name, value):
    registers[name] = value

def get(name):
    return registers[name]

def run(instructions):
    index = 0
    while index >= 0 and index < len(instructions):
        ins = instructions[index].split(" ")
        print(f"{ins} :: a={get('a')} b={get('b')}")
        if ins[0] == "hlf":
            set(ins[1], get(ins[1]) // 2)
            index += 1
        elif ins[0] == "tpl":
            set(ins[1], get(ins[1]) * 3)
            index += 1
        elif ins[0] == "inc":
            set(ins[1], get(ins[1]) + 1)
            index += 1
        elif ins[0] == "jmp":
            index += int(ins[1])
        elif ins[0] == "jie":
            reg = ins[1][0]
            if get(reg) % 2 == 0:
                index += int(ins[2])
            else:
                index += 1
        elif ins[0] == "jio":
            reg = ins[1][0]
            if get(reg) == 1:
                index += int(ins[2])
            else:
                index += 1
        else:
            print(f"unrecognized command {ins[0]}")

plines = [
    "inc a",
    "jio a, +2",
    "tpl a",
    "inc a"
]

with open("program", "r") as f:
    lines = [line.strip() for line in f.readlines()]

run(lines)
print(get("b"))