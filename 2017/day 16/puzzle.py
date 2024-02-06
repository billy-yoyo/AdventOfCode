

def exchange(s, x, y):
    x, y = min(x, y), max(x, y)
    if x == y:
        return s
    else:
        return s[:x] + s[y] + s[x+1:y] + s[x] + s[y+1:]

def partner(s, x, y):
    xi, yi = s.index(x), s.index(y)
    return exchange(s, xi, yi)

def spin(s, x):
    x = x % len(s)
    return s[-x:] + s[:-x]

string = "abcdefghijklmnop"

with open("input") as f:
    instructions = f.read().strip().split(",")

def dance(string):
    for line in instructions:
        cmd = line[0]
        if cmd == "s":
            string = spin(string, int(line[1:]))
        elif cmd == "x":
            left, right = line[1:].split("/")
            string = exchange(string, int(left), int(right))
        elif cmd == "p":
            left, right = line[1:].split("/")
            string = partner(string, left, right)
    return string

def get_cycle(string):
    last_seen = {}
    i = 0
    while True:
        if string in last_seen:
            offset = last_seen[string]
            return offset, (i - offset)

        last_seen[string] = i
        string = dance(string)
        i += 1

offset, period = get_cycle(string)
print(offset, period)

target = 1000000000
required = (target - offset) % period
print(required)
for _ in range(required):
    string = dance(string)

print(string)