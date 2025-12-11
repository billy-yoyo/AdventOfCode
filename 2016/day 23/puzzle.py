from collections import defaultdict

def try_int(x):
    try:
        return int(x)
    except:
        return x

def val(x, state):
    if isinstance(x, int):
        return x
    else:
        return state[x]

def copy(x, y):
    def cmd(pointer, state, cmds):
        if isinstance(y, str):
            state[y] = val(x, state)
        return 1
    return cmd, lambda: jump_if(x, y)

def increment(x):
    def cmd(pointer, state, cmds):
        state[x] += 1
        return 1
    return cmd, lambda: decrement(x)

def decrement(x):
    def cmd(pointer, state, cmds):
        state[x] -= 1
        return 1
    return cmd, lambda: increment(x)

def jump_if(x, y):
    def cmd(pointer, state, cmds):
        if val(x, state) != 0:
            return val(y, state)
        return 1
    return cmd, lambda: copy(x, y)

def toggle(x):
    def cmd(pointer, state, cmds):
        index = pointer + val(x, state)
        if 0 <= index < len(cmds):
            cmds[index] = cmds[index][1]()
        return 1
    return cmd, lambda: increment(x)


def compile_command(cmd):
    if cmd[0] == "cpy":
        return copy(try_int(cmd[1]), try_int(cmd[2]))
    elif cmd[0] == "inc":
        return increment(cmd[1])
    elif cmd[0] == "dec":
        return decrement(cmd[1])
    elif cmd[0] == "jnz":
        return jump_if(try_int(cmd[1]), try_int(cmd[2]))
    elif cmd[0] == "tgl":
        return toggle(try_int(cmd[1]))
    else:
        raise Exception(f"invalid command {cmd}")


with open("input") as f:
    data = f.read().strip().split("\n")

commands = [compile_command(x.split(" ")) for x in data]
state = defaultdict(int)
state["a"] = 12

pointer = 0
while pointer < len(commands):
    pointer += commands[pointer][0](pointer, state, commands)

print(state["a"])
