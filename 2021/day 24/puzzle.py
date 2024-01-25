from collections import defaultdict

commands = {}

def command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator

def val(env, x):
    try:
        return int(x)
    except:
        return env[x]

@command("inp")
def inp(env, a):
    env[a] = next(env["inputs"])

@command("add")
def add(env, a, b):
    env[a] += val(env, b)

@command("mul")
def mul(env, a, b):
    env[a] *= val(env, b)

@command("div")
def div(env, a, b):
    env[a] //= val(env, b)

@command("mod")
def mod(env, a, b):
    env[a] %= val(env, b)

@command("eql")
def eql(env, a, b):
    if env[a] == val(env, b):
        env[a] = 1
    else:
        env[a] = 0

def run(env, cmd):
    executor = commands[cmd[0]]
    executor(env, *cmd[1:])

def run_all(env, cmds):
    for cmd in cmds:
        run(env, cmd)

def execute_for_input(cmds, input):
    env = {
        "w": 0, "x": 0, "y": 0, "z": 0,
        "inputs": iter([int(x) for x in input])
    }
    run_all(env, cmds)
    return env["z"]

inputs = iter([int(x) for x in "13579246899999"])

with open("testinput") as f:
    cmds = [x.strip().split(" ") for x in f]

print(execute_for_input(cmds, "12934998949199"))