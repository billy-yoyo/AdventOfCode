from collections import defaultdict

env = defaultdict(int)

commands = {}

count_cache = [0]
def count():
    n = count_cache[0]
    count_cache[0] += 1
    return n

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


class Input:
    def __init__(self, index):
        self.index = index
    
    def __str__(self):
        return f"Input({self.index})"

class Add:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __str__(self) -> str:
        return f"Add({self.a} + {self.b})"

class Mul:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __str__(self) -> str:
        return f"Mul({self.a} * {self.b})"

class Div:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f"Div({self.a} // {self.b})"

class Mod:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __str__(self):
        return f"Mod({self.a} % {self.b})"

class Eql:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f"Eql({self.a} == {self.b})"


@command("inp")
def inp(a):
    env[a] = Input(count())

@command("add")
def add(a, b):
    env[a] = Add(env[a], val(b))

@command("mul")
def mul(a, b):
    env[a] = Mul(env[a], val(b))

@command("div")
def div(a, b):
    env[a] = Div(env[a], val(b))

@command("mod")
def mod(a, b):
    env[a] = Mod(env[a], val(b))

@command("eql")
def eql(a, b):
    env[a] = Eql(env[a], val(b))

def run(cmd):
    print(f"running cmd {cmd}")
    executor = commands[cmd[0]]
    executor(*cmd[1:])

def run_all(cmds):
    for cmd in cmds:
        run(cmd)

with open("input") as f:
    cmds = [x.strip().split(" ") for x in f]

run_all(cmds)

print(env["z"])



