
with open("data") as f:
  grid = [x.strip() for x in f if x.strip()]

width = len(grid[0])
height = len(grid)

def cell(x, y):
  return grid[y][x]

def find_start():
  for y in range(height):
    for x in range(width):
      if cell(x, y) == "S":
        return (x, y)
  return None

start = find_start()

totals = [[0] * width for _ in range(height)]
splits = 0
for y in range(height - 1):
  for x in range(width):
    c = cell(x, y)
    if c == "S":
      totals[y + 1][x] += 1
    elif totals[y][x] > 0 and c == ".":
      nextc = cell(x, y + 1)
      if nextc == "^":
        splits += 1
        totals[y + 1][x - 1] += totals[y][x]
        totals[y + 1][x + 1] += totals[y][x]
      else:
        totals[y + 1][x] += totals[y][x]

print(sum(totals[-1]))
print(splits)