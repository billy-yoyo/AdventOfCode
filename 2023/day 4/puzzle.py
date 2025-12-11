from collections import defaultdict

repeats = defaultdict(lambda: 1)

total = 0
with open("input") as f:
    for i, line in enumerate(f):
        left, right = [set([int(x.strip()) for x in side.strip().split()]) for side in line.strip().split(":")[1].strip().split("|")]
        intersection = len(left & right)
        for j in range(intersection):
            repeats[i+j+1] += repeats[i]
        if intersection > 0:
            total += 2 ** (intersection - 1)

print(total)
print(sum(repeats.values()))
