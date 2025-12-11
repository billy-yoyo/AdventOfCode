
total = 0
with open("input") as f:
    numbers = [int(x) for x in f.read().strip().split("\n")]

visited = {0}
i = 0
while True:
    total += numbers[i]
    if total in visited:
        print(total)
        break
    visited |= {total}
    i = (i + 1) % len(numbers)
