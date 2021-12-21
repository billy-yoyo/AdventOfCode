

with open("testinput") as f:
    input = f.read()

algo, image = input.split("\n\n")
algo = algo.strip().replace("\n", "").replace(" ", "")
image_lines = [line.strip() for line in image.strip().split("\n")]
image = {}
charmap = {
    ".": "0",
    "#": "1"
}

for y, line in enumerate(image_lines):
    for x, c in enumerate(line):
        image[(x, y)] = c

def encode(x, y, default):
    chars = "".join([charmap[image.get((x + dx, y + dy), default)] for dy in range(-1, 2) for dx in range(-1, 2)])
    return algo[int(chars, 2)]

def tick(count):
    default = "."# if count % 2 == 0 else "#"
    new_image = {}
    positions = set([k for k, v in image.items() if v == "#"])
    for x, y in list(positions):
        subpos = [(x + dx, y + dy) for dx in range(-2, 3) for dy in range(-2, 3)]
        positions |= set(subpos)
    for x, y in positions:
        new_image[(x, y)] = encode(x, y, default)
    return new_image

def size():
    return sum([1 for x in image.values() if x == "#"])

def show():
    minx = min(x for x, y in image.keys())
    miny = min(y for x, y in image.keys())
    maxx = max(x for x, y in image.keys())
    maxy = max(y for x, y in image.keys())
    print("\n".join("".join(image.get((x, y), ".") for x in range(minx, maxx + 1)) for y in range(miny, maxy + 1)))

print(size())
for i in range(50):
    image = tick(i)
    print(size())
show()