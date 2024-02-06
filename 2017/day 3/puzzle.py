import math
from collections import defaultdict

def unspiral(n):
    ns = math.ceil(math.sqrt(n))
    if ns % 2 == 0:
        ns += 1
    
    if ns == 1:
        return (0, 0)

    offset = n - ((ns - 2) ** 2)
    half_ns = ns // 2
    partial_offset = ((offset - 1) % (ns - 1)) + 1
    if offset <= ns - 1:
        return (half_ns, half_ns - partial_offset)
    elif offset <= (ns - 1) * 2: 
        return (half_ns - partial_offset, -half_ns)
    elif offset <= (ns - 1) * 3:
        return (-half_ns, partial_offset - half_ns)
    else:
        return (partial_offset - half_ns, half_ns)

x, y = unspiral(325489)
print(abs(x) + abs(y))

grid = defaultdict(int)
grid[unspiral(1)] = 1
i = 1
last_value = 0
while last_value < 325489:
    i += 1
    x, y = unspiral(i)
    cur_total = 0
    for ox in range(-1, 2):
        for oy in range(-1, 2):
            if ox == 0 and oy == 0:
                continue
            cur_total += grid[(x + ox, y + oy)]
    grid[(x, y)] = cur_total
    last_value = cur_total

print(last_value)
