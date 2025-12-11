from itertools import combinations

with open("data") as f:
  data = f.read().strip().split("\n")

width, height = len(data[0]), len(data)
freqs = set("".join(data))
freqs.remove(".")

freq_locs = {freq: [
  (x, y) for y, row in enumerate(data) for x, c in enumerate(row) if c == freq
] for freq in freqs}

antinodes = set()

def add_antinode(x, y):
  if 0 <= x < width and 0 <= y < height:
    antinodes.add((x, y))
    return True
  return False

for freq in freqs:
  locs = freq_locs[freq]
  for x, y in locs:
    add_antinode(x, y)
  for ai, bi in combinations(range(len(locs)), 2):
    a, b = locs[ai], locs[bi]

    dx, dy = a[0] - b[0], a[1] - b[1]
    i = 0
    while True:
      a_changed = add_antinode(a[0] + (dx * i), a[1] + (dy * i))
      b_changed = add_antinode(b[0] - (dx * i), b[1] - (dy * i))
      if not a_changed and not b_changed:
        break
      i += 1

print_data = [["." for x in range(width)] for y in range(height)]
for x, y in antinodes:
  print_data[y][x] = "#"

for freq, locs in freq_locs.items():
  for x, y in locs:
    print_data[y][x] = freq

#print("\n".join("".join(x) for x in print_data))


print(len(antinodes))

