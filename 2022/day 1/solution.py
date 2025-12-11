
with open("puzzle") as f:
    data = f.read()


def parse(data):
    elves = data.split("\n\n")
    return [[int(x) for x in elf.strip().split("\n")] for elf in elves]

elves = parse(data)
elf_totals = sorted([sum(elf) for elf in elves])

print(sum(elf_totals[-3:]))

print(sum(sorted([sum(int(x)for x in e.split())for e in open("puzzle").read().split("\n\n")])[-3:]))
