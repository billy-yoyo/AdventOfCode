
def format(c, *vals):
    return f"{r[c]} = {' '.join(str(x) for x in vals)}"

r = "abcdPf"
commands = {
    "addr": lambda a, b, c: format(c, r[a], "+", r[b]),
    "addi": lambda a, b, c: format(c, r[a], "+", b),
    "mulr": lambda a, b, c: format(c, r[a], "*", r[b]),
    "muli": lambda a, b, c: format(c, r[a], "*", b),
    "banr": lambda a, b, c: format(c, r[a], "&", r[b]),
    "bani": lambda a, b, c: format(c, r[a], "&", b),
    "borr": lambda a, b, c: format(c, r[a], "|", r[b]),
    "bori": lambda a, b, c: format(c, r[a], "|", b),
    "setr": lambda a, b, c: format(c, r[a]),
    "seti": lambda a, b, c: format(c, a),
    "gtir": lambda a, b, c: format(c, a, ">", r[b]),
    "gtri": lambda a, b, c: format(c, r[a], ">", b),
    "gtrr": lambda a, b, c: format(c, r[a], ">", r[b]),
    "eqir": lambda a, b, c: format(c, a, "==", r[b]),
    "eqri": lambda a, b, c: format(c, r[a], "==", b),
    "eqrr": lambda a, b, c: format(c, r[a], "==", r[b]),
}

with open("input") as f:
    lines = f.read().strip().split("\n")[1:]

with open("transformed", "w") as f:
    for line in lines:
        key, a, b, c = line.strip().split(" ")
        f.write(commands[key](int(a), int(b), int(c)) + "\n")


