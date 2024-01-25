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
    
def compute(x, values):
    if isinstance(x, int):
        return x
    else:
        return x.compute(values)


class Input:
    def __init__(self, index):
        self.index = index

    def compute(self, values):
        if values[self.index] is not None:
            return values[self.index]
        return self
    
    def __str__(self):
        return f"Input({self.index})"

class Add:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, values):
        left, right = compute(self.a, values), compute(self.b, values)
        if isinstance(left, int) and isinstance(right, int):
            return left + right
        else:
            return Add(left, right)
    
    def __str__(self) -> str:
        return f"Add({self.a} + {self.b})"

class Mul:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, values):
        left, right = compute(self.a, values), compute(self.b, values)
        if isinstance(left, int) and isinstance(right, int):
            return left + right
        elif isinstance(left, int) and isinstance(right, Add):
            return Add(
                Mul(right.a, left).compute(values),
                Mul(right.b, left).compute(values)
            )
        elif isinstance(left, Add) and isinstance(right, int):
            return Add(
                Mul(left.a, right).compute(values),
                Mul(left.b, right).compute(values)
            )
        elif isinstance(left, Div) and isinstance(right, int):
            return Div(
                Mul(left.a, right).compute(values),
                left.b
            )
        elif isinstance(left, int) and isinstance(right, Div):
            return Div(
                Mul(right.a, left).compute(values),
                right.b
            )
        else:
            return Add(left, right)
    
    def __str__(self) -> str:
        return f"Mul({self.a} * {self.b})"

class Div:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, values):
        left, right = compute(self.a, values), compute(self.b, values)
        if isinstance(left, int) and isinstance(right, int):
            return left // right
        elif isinstance(left, Add) and isinstance(right, int):
            return Add(
                Div(left.a, right).compute(values),
                Div(left.b, right).compute(values)
            )
        elif isinstance(left, Mul) and isinstance(right, int):
            if isinstance(left.a, int):
                return Mul(
                    left.a // right,
                    left.b
                )
            elif isinstance(left.b, int):
                return Mul(
                    left.a,
                    left.b // right
                )
            else:
                return Div(left, right)
        else:
            return Div(left, right)

    def __str__(self):
        return f"Div({self.a} // {self.b})"

class Mod:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, values):
        left, right = compute(self.a, values), compute(self.b, values)
        if isinstance(left, int) and isinstance(right, int):
            return left % right
        else:
            return Mod(left, right)
    
    def __str__(self):
        return f"Mod({self.a} % {self.b})"

class Eql:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, values):
        left, right = compute(self.a, values), compute(self.b, values)
        if isinstance(left, int) and isinstance(right, int):
            return left == right
        else:
            return Eql(left, right)

    def __str__(self):
        return f"Eql({self.a} == {self.b})"

values = [9] * 14
values[0] = None

@command("inp")
def inp(a):
    i = count()
    value = values[i]
    if value is not None:
        env[a] = value
    else:
        env[a] = Input(i)

@command("add")
def add(a, b):
    env[a] = Add(env[a], val(b)).compute(values)

@command("mul")
def mul(a, b):
    env[a] = Mul(env[a], val(b)).compute(values)

@command("div")
def div(a, b):
    env[a] = Div(env[a], val(b)).compute(values)

@command("mod")
def mod(a, b):
    env[a] = Mod(env[a], val(b)).compute(values)

@command("eql")
def eql(a, b):
    env[a] = Eql(env[a], val(b)).compute(values)

def run(cmd):
    print(f"running cmd {cmd}")
    executor = commands[cmd[0]]
    executor(*cmd[1:])
    print(env["z"])

def run_all(cmds):
    for cmd in cmds:
        run(cmd)

with open("input") as f:
    cmds = [x.strip().split(" ") for x in f]

run_all(cmds)

print("evaluating...")
env["z"].compute([9] * 14)



