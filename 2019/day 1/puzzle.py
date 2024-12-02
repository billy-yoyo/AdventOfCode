
with open("input") as f:
    ns = [int(x) for x in f.read().strip().split("\n")]

def recful(x):
    total = 0
    while x > 0:
        x = max(0, (x // 3) - 2)
        total += x
    return total

print(sum(recful(x) for x in ns))

