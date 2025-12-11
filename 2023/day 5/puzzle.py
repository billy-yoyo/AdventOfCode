from collections import defaultdict


with open("input") as f:
    sections = f.read().strip().split("\n\n")

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

seeds = [int(x) for x in sections[0].split(":")[1].split()]
target_ranges = [[x, x + y] for x,y in chunks(seeds, 2)]

targets = list(seeds)

mapping = defaultdict(lambda: defaultdict(dict))

def apply_mapping(x, ranges):
    for source_start, dest_start, size in ranges:
        if x >= dest_start and x < dest_start + size:
            return source_start + (x - dest_start)
    return x

def apply_ranged_mapping(target_range, ranges):
    x0, x1 = target_range
    covered = []
    new_ranges = []
    for source_start, dest_start, size in ranges:
        if x0 >= dest_start and x0 < dest_start + size:
            if x1 <= dest_start + size:
                return [[source_start + (x0 - dest_start), source_start + (x1 - dest_start)]]
            else:
                covered.append([x0, dest_start + size])
                new_ranges.append([source_start + (x0 - dest_start), source_start + size])
        elif x1 > dest_start and x1 <= dest_start + size:
            covered.append([dest_start, x1])
            new_ranges.append([source_start, source_start + (x1 - dest_start)])
        elif x0 < dest_start and x1 > dest_start + size:
            covered.append([dest_start, dest_start + size])
            new_ranges.append([source_start, source_start + size])
    
    # look for any uncovered sections
    covered = sorted(covered, key = lambda x: x[0])
    last_end = x0
    for y0, y1 in covered:
        if y0 != last_end:
            new_ranges.append([last_end, y0])
        
        last_end = y1
    if last_end != x1:
        new_ranges.append([last_end, x1])

    return new_ranges


for x in sections[1:]:
    lines = x.strip().split("\n")
    from_type, to_type = lines[0].split(" map")[0].split("-to-")
    ranges = [[int(y) for y in line.strip().split()] for line in lines[1:]]

    
    targets = [apply_mapping(target, ranges) for target in targets]
    new_target_ranges = []
    for target_range in target_ranges:
        new_target_ranges += apply_ranged_mapping(target_range, ranges)
    target_ranges = new_target_ranges
    #print(targets)

    mapping[from_type][to_type] = ranges

#print(min(targets))
print(min(x[0] for x in target_ranges))
