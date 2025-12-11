from collections import defaultdict

def val(registers, y):
    if isinstance(y, int):
        return y
    else:
        return registers[y]

def try_int(x):
    try:
        return int(x)
    except:
        return x

def set(x, y):
    def cmd(registers, in_stack, out_stack):
        registers[x] = val(registers, y)
        return 1
    return cmd

def add(x, y):
    def cmd(registers, in_stack, out_stack):
        registers[x] += val(registers, y)
        return 1
    return cmd

def mul(x, y):
    def cmd(registers, in_stack, out_stack):
        registers[x] *= val(registers, y)
        return 1
    return cmd

def mod(x, y):
    def cmd(registers, in_stack, out_stack):
        registers[x] %= val(registers, y)
        return 1
    return cmd

def jump(x, y):
    def cmd(registers, in_stack, out_stack):
        if val(registers, x) > 0:
            return val(registers, y)
        return 1
    return cmd

def push(x):
    def cmd(registers, in_stack, out_stack):
        #print(f"sending {val(registers, x)}")
        out_stack.append(val(registers, x))
        return 1
    return cmd

def pop_if(x):
    def cmd(registers, in_stack, out_stack):
        if len(in_stack) > 0:
            registers[x] = in_stack.pop(0)
            return 1
        return 0
    return cmd

def parse_command(command):
    kwd = command[0]
    match kwd:
        case "set": return set(command[1], try_int(command[2]))
        case "add": return add(command[1], try_int(command[2]))
        case "mul": return mul(command[1], try_int(command[2]))
        case "mod": return mod(command[1], try_int(command[2]))
        case "jgz": return jump(try_int(command[1]), try_int(command[2]))
        case "snd": return push(try_int(command[1]))
        case "rcv": return pop_if(try_int(command[1]))
    raise Exception(f"invalid command {kwd}")

instructions = []
with open("input") as f:
    for line in f.read().strip().split("\n"):
        command = line.split(" ")
        instructions.append(parse_command(command))

left_stack, right_stack = [], []

computers = (
    (defaultdict(int), left_stack, right_stack),
    (defaultdict(int), right_stack, left_stack)
)
for i in range(2):
    computers[i][0]["p"] = i
pointers = [0, 0]
total = 0

last_waiting = False
while any(0 <= p < len(instructions) for p in pointers):
    waiting = 0
    terminated = 0
    for i, p in enumerate(pointers):
        if p < 0 or p >= len(instructions):
            terminated += 1
            continue
        size_before = len(left_stack)
        pdiff = instructions[p](*computers[i])
        size_after = len(left_stack)
        if size_after > size_before:
            #print(f"sent {left_stack[-1]}")
            total += 1

        if pdiff == 0:
            waiting += 1
        else:
            pointers[i] += pdiff
    
    if waiting == 2:
        if last_waiting:
            break
        else:
            last_waiting = True
    elif waiting == 1 and terminated == 1:
        break
    else:
        last_waiting = False
        

print(total)





