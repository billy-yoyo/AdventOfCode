
with open("data") as f:
    instructions = [
        (name, int(n)) for name, n in [x.strip().split() for x in f.read().split("\n")]
    ]

def calculate_with_change(changed):
    if instructions[changed] == "acc":
        return None

    visited = {}
    acc, i = 0, 0
    while i < len(instructions):
        if i in visited:
            # found infinite loop
            return None

        name, n = instructions[i]
        if i == changed:
            if name == "nop":
                name = "jmp"
            else:
                name = "nop"

        visited[i] = True

        if name == "nop":
            i += 1
        elif name == "acc":
            acc += n
            i += 1
        elif name == "jmp":
            i += n
        else:
            print(f"unknown instruction {name}")

    return acc

for i in range(len(instructions)):
    acc = calculate_with_change(i)
    if acc is not None:
        print(acc)
        break
