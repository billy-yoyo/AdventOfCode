
env = {}

commands = {}

def command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator

def val(x):
    try:
        return int(x)
    except:
        return env[x]

@command("inp")
def inp(a):
    env[a] = next(inputs)

@command("add")
def add(a, b):
    env[a] += val(b)

@command("mul")
def mul(a, b):
    env[a] *= val(b)

@command("div")
def div(a, b):
    env[a] //= val(b)

@command("mod")
def mod(a, b):
    env[a] %= val(b)

@command("eql")
def eql(a, b):
    if env[a] == val(b):
        env[a] = 1
    else:
        env[a] = 0

def run(cmd):
    executor = commands[cmd[0]]
    executor(*cmd[1:])

def run_all(cmds):
    for cmd in cmds:
        run(cmd)


inputs = iter([int(x) for x in "13579246899999"])

with open("testinput") as f:
    cmds = [x.strip().split(" ") for x in f]

run_all(cmds)
print(env)