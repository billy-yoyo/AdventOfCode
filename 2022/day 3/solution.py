from collections import defaultdict

data = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()

with open("puzzle") as f:
    data = f.read()

lines = data.split("\n")
sacks = [[line[:len(line)//2], line[len(line)//2:]] for line in lines]

priority = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

common = [next(item for item in left if item in right) for left, right in sacks]
values = [priority.index(item) + 1 for item in common]
total = sum(values)

print(total)


total2 = 0
for i in range(0, len(lines), 3):
    counts = defaultdict(int)
    for j in range(3):
        for c in set(lines[i+j]):
            counts[c] += 1
    for item, count in counts.items():
        if count == 3:
            total2 += priority.index(item) + 1
            break

print(total2)