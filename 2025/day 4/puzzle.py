
with open("example") as f:
  data = [list(x.strip()) for x in f.read().strip().split("\n")]

width = len(data[0])
height = len(data)

def cell(x, y):
  if 0 <= y < height and 0 <= x < width:
    return data[y][x]
  return "."

dirs = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0]

def find_removeable(positions):
  stack = set()
  for x, y in positions:
    if sum(1 for dx, dy in dirs if cell(x + dx, y + dy) == "@") < 4:
      stack.add((x, y))
  return stack


count = 0
stack = find_removeable([(x, y) for x in range(width) for y in range(height) if cell(x, y) == "@"])
while len(stack):
  count += len(stack)
  neighbours = set()
  for x, y in stack:
    for dx, dy in dirs:
      npos = x + dx, y + dy
      if npos not in stack and cell(*npos) == "@":
        neighbours.add(npos)
    data[y][x] = "."
  stack = find_removeable(neighbours)


print(count)
