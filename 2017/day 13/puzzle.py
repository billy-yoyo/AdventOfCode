
with open("input") as f:
    layers = [[int(x) for x in line.split(": ")] for line in f.read().strip().split("\n")]

layers = [(i, x, (x - 1) * 2) for i, x in layers]

print(sum(x * layer for layer, x, period in layers if layer % period == 0 ))

def is_valid(start_time):
    for layer, _, period in layers:
        if (start_time + layer) % period == 0:
            return False
    return True

i = 0
while not is_valid(i):
    i += 1

print(i)

