from collections import defaultdict

def perform_twists(data, inputs, pointer, skip_size):
    size = len(data)
    for input in inputs:
        for i in range(input // 2):
            ai, bi = (pointer + i) % size, (pointer + (input - (i + 1))) % size
            data[ai], data[bi] = data[bi], data[ai]
        pointer += input + skip_size
        skip_size += 1
    return pointer, skip_size

def pad_left(s, c, x):
    return (c * (x - len(s))) + s 

def hexify(x):
    return pad_left(hex(x)[2:], "0", 2)

def binaryify(x):
    return pad_left(bin(x)[2:], "0", 4)

def hash_bytes(inputs, represent):
    data = list(range(256))
    inputs += [17, 31, 73, 47, 23]
    pointer, skip_size = 0, 0
    for _ in range(64):
        pointer, skip_size = perform_twists(data, inputs, pointer, skip_size)
    
    chunks = []
    for chunk in range(16):
        chunk_start, chunk_end = chunk * 16, (chunk + 1) * 16
        chunk_value = data[chunk_start]
        for i in range(chunk_start + 1, chunk_end):
            chunk_value ^= data[i]
        chunks.append(chunk_value)
    
    return "".join([represent(x) for x in chunks])

def hash(string):
    return hash_bytes([ord(c) for c in string], hexify)

hex_chars = "0123456789abcdef"
def hash_binary(string):
    return "".join([binaryify(hex_chars.index(x)) for x in hash(string)])

key = "hxtvlmkl"
#key = "flqrgnkx"

region_ids = defaultdict(int)
region_locations = defaultdict(set)

width = 128
height = 128

total = 0 
next_region_id = 1
for y in range(height):
    row = hash_binary(f"{key}-{y}")[:width]
    #print(row.replace("0", "."))

    indexed_row = [x for x, c in enumerate(row) if c == "1"]
    sub_regions = []
    next_region = None
    for x in indexed_row:

        if next_region is None:
            next_region = [x, x]
        elif x == next_region[1] + 1:
            next_region[1] = x
        else:
            sub_regions.append(next_region)
            next_region = [x, x]
    sub_regions.append(next_region)

    for start, end in sub_regions:
        sub_region_ids = set(region_ids[(x, y - 1)] for x in range(start, end + 1)) - {0}
        if len(sub_region_ids) == 0:
            region_id = next_region_id
            next_region_id += 1
        elif len(sub_region_ids) == 1:
            region_id = next(iter(sub_region_ids))
        else:
            sub_region_ids = list(sub_region_ids)
            region_id = sub_region_ids[0]
            for other_region_id in sub_region_ids[1:]:
                for ox, oy in region_locations[other_region_id]:
                    region_ids[(ox, oy)] = region_id
                    region_locations[region_id] |= {(ox, oy)}
                region_locations[other_region_id] = set()
        for x in range(start, end + 1):
            region_ids[(x, y)] = region_id
            region_locations[region_id] |= {(x, y)}

    total += row.count("1")
#print("\n")
region_chars = ".123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#print("\n".join("".join(region_chars[region_ids[(x, y)] % len(region_chars)] for x in range(30, 50)) for y in range(5)))

def check():
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for x in range(width):
        for y in range(height):
            if region_ids[(x, y)] == 0:
                continue
            neighbour_regions = (set(region_ids[(x + ox, y + oy)] for ox, oy in offsets) | {region_ids[(x, y)]}) - {0}
            if len(neighbour_regions) > 1:
                print(f"location {x}, {y} has different regions next to each other: {neighbour_regions}")
#check()

print(total)
print(len([x for x in region_locations.values() if len(x) > 0]))
