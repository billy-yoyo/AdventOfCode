from collections import defaultdict

with open("data") as f:
  data = f.read().strip().split("\n")

w = len(data[0])
h = len(data)

start = next((x, y) for x in range(w) for y in range(h) if data[y][x] == "S")
end = next((x, y) for x in range(w) for y in range(h) if data[y][x] == "E")

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

path = [start]
pos = start
while pos != end:
  for ox, oy in offsets:
    x, y = pos[0] + ox, pos[1] + oy
    if data[y][x] != "#" and (x, y) not in path:
      pos = (x, y)
      path.append(pos)

distances = {}
for i, pos in enumerate(reversed(path)):
  distances[pos] = i

def smallest_dist_in_range(pos, max_dist):
  steps = max_dist
  stack = [pos]
  for _ in range(steps):
    next_stack = []
    for x, y in stack:
      for ox, oy in offsets:
        next_stack.append((x + ox, y + oy))
    stack = next_stack
  
  for opos in set(stack):
    if opos in distances:
      yield distances[opos]


def pt1():
  totals = defaultdict(int)
  total = 0


  for pos in path:
    distance = distances[pos]
    for cheat_dist in smallest_dist_in_range(pos, 2):
      if cheat_dist >= distance:
        continue

      gap = abs(distance - cheat_dist) - 2
      if gap > 2:
        #print(f"at {pos} you can cheat {gap}")
        totals[gap] += 1

      if gap >= 100:
        total += 1

  #print(totals)
  print(total)

def man_dist(p1, p2):
  return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def pt2():
  total = 0
  totals = defaultdict(int)
  for i, pos in enumerate(path):
    for j in range(len(path) - 1, i, -1):
      opos = path[j]
      mdist = man_dist(pos, opos)
      if mdist <= 20:
        gap = abs(distances[pos] - distances[opos]) - mdist
        #if gap >= 50:
        #  print(f"at {pos} you can cheat {gap} by jumping to {opos}")
        #  totals[gap] += 1

        if gap >= 100:
          total += 1
  
  for gap, count in sorted(totals.items()):
    print(f"{gap}: {count}")

  print(total)

pt2()