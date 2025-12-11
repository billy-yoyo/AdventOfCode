
with open("input") as f:
    data = f.read().strip().split("\n")

rules_2x = []
rules_3x = []

rotation_mappings = [
    lambda w, h, x, y: (x, y), # 0 degrees
    lambda w, h, x, y: (h - (y + 1), x), # 90 degrees
    lambda w, h, x, y: (w - (x + 1), h - (y + 1)), # 180 degrees
    lambda w, h, x, y: (y, w - (x + 1))
]

flipped_mappings = [
    lambda w, h, x, y: (x, y),
    lambda w, h, x, y: (w - (x + 1), y),
    lambda w, h, x, y: (x, h - (y + 1)),
]

def pattern_matches_exactly(pattern, rule, rotation, flipped):
    size = len(pattern)
    for y, line in enumerate(pattern):
        for x, c in enumerate(line):
            tx, ty = rotation_mappings[rotation](size, size, *flipped_mappings[flipped](size, size, x, y))
            if c != rule[ty][tx]:
                return False
    return True 

def pattern_matches(pattern, rule):
    for rotation in range(len(rotation_mappings)):
        for flipped in range(len(flipped_mappings)):
            if pattern_matches_exactly(pattern, rule, rotation, flipped):
                return True
    return False

def expand_pattern(pattern, rules):
    for rule, expanded in rules:
        if pattern_matches(pattern, rule):
            return expanded

for line in data:
    rstring, pstring = line.split("=>")
    rule = rstring.strip().split("/")
    pattern = pstring.strip().split("/")
    if len(rule[0]) == 2:
        rules_2x.append((rule, pattern))
    else:
        rules_3x.append((rule, pattern))

def expand(data):
    if len(data) % 2 == 0:
        grid_size = 2
        rules = rules_2x
    else:
        grid_size = 3
        rules = rules_3x
    
    chunks = len(data) // grid_size
    lines = [[] for _ in range(chunks * (grid_size + 1))]
    for chunk_y in range(chunks):
        for chunk_x in range(chunks):
            chunk = [[
                data[y][x] for x in range(chunk_x * grid_size, (chunk_x + 1) * grid_size)
            ] for y in range(chunk_y * grid_size, (chunk_y + 1) * grid_size)]
            #print(f"{chunk_x=} {chunk_y=}")
            #print_data(chunk)
            expanded_chunk = expand_pattern(chunk, rules)

            for i, line in enumerate(expanded_chunk):
                lines[(chunk_y * (grid_size + 1)) + i] += line
    return lines

def print_data(data):
    print("\n".join("".join(line) for line in data))

initial_data = [
    [".", "#", "."],
    [".", ".", "#"],
    ["#", "#", "#"]
]

data = initial_data
for _ in range(18):
    #print_data(data)
    #print("")
    data = expand(data)

print(sum(l.count("#") for l in data))


