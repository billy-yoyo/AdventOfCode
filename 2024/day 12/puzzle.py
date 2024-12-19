from collections import defaultdict

with open("data") as f:
  data = f.read().strip().split("\n")

width = len(data[0])
height = len(data)

region_index = defaultdict(int)
visited = set()

transformed_data = [list(row) for row in data]

def get(data, x, y):
  if 0 <= x < width and 0 <= y < height:
    return data[y][x]
  return ""

offs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def mark_region(x, y, region, region_index):
  if (x, y) in visited:
    return
  
  visited.add((x, y))
  transformed_data[y][x] = f"{region}{region_index}"

  for ox, oy in offs:
    if get(data, x + ox, y + oy) == region:
      mark_region(x+ox, y+oy, region, region_index)

for x in range(width):
  for y in range(height):
    if (x, y) not in visited:
      region = get(data, x, y)
      ri = region_index[region]
      region_index[region] += 1
      mark_region(x, y, region, ri)

areas = defaultdict(int)
perims = defaultdict(int)
perim_sets = defaultdict(set)

for y, row in enumerate(transformed_data):
  for x, c in enumerate(row):
    areas[c] += 1
    for i, (ox, oy) in enumerate(offs):
      if get(transformed_data, x + ox, y + oy) != c:
        perims[c] += 1
        perim_sets[c].add((x + ox, y + oy, i))

def count_sides(pset):
  clone = set(pset)
  sides = 0
  while clone:
    sx, sy, si = clone.pop()
    sides += 1
    for ox, oy in offs:
      px, py = sx + ox, sy + oy
      while (px, py, si) in clone:
        clone.remove((px, py, si))
        px, py = px + ox, py + oy
  return sides

total = 0
total_2 = 0
for key, area in areas.items():
  #print(f"{key}: {area} x {count_sides(perim_sets[key])}")
  total += area * perims[key]
  total_2 += area * count_sides(perim_sets[key])

print(total)
print(total_2)


