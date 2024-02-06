
with open("input") as f:
    offsets = [int(x) for x in f.read().strip().split("\n")]

pointer = 0
steps = 0
while 0 <= pointer < len(offsets):
    steps += 1
    next_pointer = pointer + offsets[pointer]
    offsets[pointer] += 1 if offsets[pointer] < 3 else -1
    pointer = next_pointer
print(steps)
