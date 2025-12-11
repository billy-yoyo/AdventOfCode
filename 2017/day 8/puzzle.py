from collections import defaultdict

with open("input") as f:
    data = f.read().strip().split("\n")

registers = defaultdict(int)

operator_funcs = {
    ">": lambda a,b: a > b,
    "<": lambda a,b: a < b,
    ">=": lambda a,b: a >= b,
    "<=": lambda a,b: a <= b,
    "!=": lambda a,b: a != b,
    "==": lambda a,b: a == b
}

def check_condition(left, right, operator):
    return operator_funcs[operator](registers[left], right)

def do_verb(target, amount, verb):
    registers[target] += (-amount if verb == "dec" else amount)

highest_ever = 0
for line in data:
    action, condition = line.split("if")
    action = action.strip().split(" ")
    condition = condition.strip().split(" ")
    target, verb, amount = action[0], action[1], int(action[2])
    left, operator, right = condition[0], condition[1], int(condition[2])

    if check_condition(left, right, operator):
        do_verb(target, amount, verb)
        highest_ever = max(highest_ever, max(registers.values()))

print(max(registers.values()))
print(highest_ever)

