
with open("data") as f:
  rows = [x.strip() for x in f.read().strip().split("\n")]

x_locations = [(x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == "X"]
directions = [
  (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)
]

def get(x, y):
  if x < 0 or y < 0 or x >= len(rows[0]) or y >= len(rows):
    return ""
  return rows[y][x]

word = "XMAS"

def is_xmas(x, y, dx, dy):
  for i in range(1, 4):
    nx, ny = x + (dx * i), y + (dy * i)
    if nx < 0 or ny < 0 or nx >= len(rows[0]) or ny >= len(rows):
      return False
    if rows[ny][nx] != word[i]:
      return False
  return True

count_xmas = 0
for x, y in x_locations:
  for dx, dy in directions:
    if is_xmas(x, y, dx, dy):
      count_xmas += 1
  
print(count_xmas)

a_locations = [(x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == "A"]


count_mas = 0
for x, y in a_locations:
  diag1 = "".join([get(x - 1, y - 1), get(x + 1, y + 1)])
  diag2 = "".join([get(x - 1, y + 1), get(x + 1, y - 1)])

  if (diag1 == "MS" or diag1 == "SM") and (diag2 == "MS" or diag2 == "SM"):
    count_mas += 1
  
print(count_mas)