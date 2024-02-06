
def count_pairs(s):
    total = 0
    for i, c in enumerate(s):
        if c == s[(i + (len(s) // 2)) % len(s)]:
            total += int(c)
    return total

with open("input") as f:
    data = f.read().strip()

print(count_pairs(data))
