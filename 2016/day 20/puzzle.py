
with open("input") as f:
    ranges = [[int(x) for x in line.split("-")] for line in f.read().strip().split("\n")]

ranges = sorted(ranges)
print(ranges)

collapsed_ranges = []
current_range = list(ranges[0])
for r in ranges[1:]:
    if r[0] - 1 <= current_range[1]:
        current_range[1] = max(current_range[1], r[1])
    else:
        collapsed_ranges.append(current_range)
        current_range = list(r)

collapsed_ranges.append(current_range)

print(collapsed_ranges)
print(collapsed_ranges[0][1] + 1)

range_max = 4294967295
#range_max = 15
total = 0
for start, end in collapsed_ranges:
    total += (end + 1 - start)

print(range_max + 1 - total)
