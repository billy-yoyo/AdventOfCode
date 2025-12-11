from collections import defaultdict, deque

with open("data") as f:
  data = [[int(x) for x in row] for row in f.read().strip().split("\n")]

width = len(data[0])
height = len(data)

def get(x, y):
  if 0 <= x < width and 0 <= y < height:
    return data[y][x]
  return 20

offs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

end_points = defaultdict(list)

def calc_endpoints(start):
  queue = deque([start])
  visited = set()
  while queue:
    x, y = queue.pop()
    if (x, y) in visited:
      continue
    
    end_points[(x, y)].append(start)
    value = get(x, y)

    if value == 0:
      continue

    for ox, oy in offs:
      ovalue = get(x + ox, y + oy)
      if ovalue == value - 1:
        queue.append((x + ox, y + oy))


zero_pos = [(x, y) for y, row in enumerate(data) for x, c in enumerate(row) if c == 0]
nine_pos = [(x, y) for y, row in enumerate(data) for x, c in enumerate(row) if c == 9]

for start in nine_pos:
  calc_endpoints(start)

total_1 = 0
total_2 = 0
for pos in zero_pos:
  total_1 += len(set(end_points[pos]))
  total_2 += len(end_points[pos])

print(total_1)
print(total_2)
