
with open("directions", "r") as f:
    directions = f.read().strip().split(", ")

def rotate(d, ins):
    new_dir = ins[0]
    if new_dir == "L":
        return (d - 1) % 4
    else:
        return (d + 1) % 4
    

def move(x, y, d, ins):
    amt = int(ins[1:])
    if d == 0:
        for i in range(1, amt + 1):
            yield (x, y + i)
    elif d == 1:
         for i in range(1, amt + 1):
            yield (x + i, y)
    elif d == 2:
         for i in range(1, amt + 1):
            yield (x, y - i)
    else:
         for i in range(1, amt + 1):
            yield (x - i, y)

visited = {}

def check_visited(x, y):
    key = f"{x}:{y}"
    #print(key)
    if key in visited:
        print(x + y)
    visited[key] = True

x, y, d = 0, 0, 0
check_visited(x, y)
for ins in directions:
    d = rotate(d, ins)
    for x, y in move(x, y, d, ins):
        check_visited(x, y)

print(x + y)