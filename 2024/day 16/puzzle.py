from collections import defaultdict

with open("data") as f:
  data = f.read().strip().split("\n")

w = len(data[0])
h = len(data)

NORTH=0
EAST=1
SOUTH=2
WEST=3

graph = defaultdict(lambda: [None, None, None, None])
dirmap = [(0, -1), (1, 0), (0, 1), (-1, 0)]

nodes = set()
for x in range(w):
  for y in range(h):
    if data[y][x] != "#":
      pattern = list(data[y+dy][x+dx] for dx,dy in dirmap)
      if pattern.count("#") != 2 or not ((pattern[NORTH] == pattern[SOUTH] == "#") or (pattern[EAST] == pattern[WEST] == "#")):
        nodes.add((x, y))

for x, y in nodes:
  for dir, (dx,dy) in enumerate(dirmap):
    fx, fy = x + dx, y + dy
    while data[fy][fx] != "#" and (fx, fy) not in nodes:
      fx += dx
      fy += dy
    if data[fy][fx] == "#":
      fx -= dx
      fy -= dy
    if fx != x or fy != y:
      graph[(x, y)][dir] = ((fx, fy), abs(fx - x) + abs(fy - y))

start = next((x, y) for y in range(h) for x in range(w) if data[y][x] == "S")
target = next((x, y) for y in range(h) for x in range(w) if data[y][x] == "E")

def between(p1, p2):
  if p1[0] == p2[0]:
    for y in range(min(p1[1], p2[1]), max(p1[1], p2[1])+1):
      yield (p1[0], y)
  else:
    for x in range(min(p1[0], p2[0]), max(p1[0], p2[0])+1):
      yield (x, p1[1])


def find_path(start, target):
  paths = [(0, start, EAST, [])]
  best_score = defaultdict(lambda: (-1, set()))
  while paths:
    next_paths = []
    for cost, pos, dir, pth in paths:
      best_so_far, best_paths = best_score[pos]
      if best_so_far == -1 or cost < best_so_far:
        pathset = set(pth)

        if pos == target:
          for i, opos in enumerate(pth[:-1]):
            for bpos in between(opos, pth[i+1]):
              pathset.add(bpos)
          
          pathset.add(pos)
          if pth:
            for bpos in between(pth[-1], pos):
              pathset.add(bpos)
        
        best_score[pos] = (cost, pathset)
      elif cost == best_so_far:
        if pos == target:
          for i, opos in enumerate(pth):
            best_paths.add(opos)
            if i < len(pth) - 1:
              for bpos in between(opos, pth[i+1]):
                best_paths.add(bpos)
          
          best_paths.add(pos)
          if pth:
            for bpos in between(pth[-1], pos):
              best_paths.add(bpos) 
      elif cost > best_so_far + 2000:
        continue
        
      if pos == target:
        continue

      for i, conn in enumerate(graph[pos]):
        if conn is None:
          continue
          
        dest_pos, dist = conn
        if dest_pos in pth:
          continue
        
        new_cost = cost + dist
        if dir == i:
          pass
        elif dir == ((i + 1) % 4) or dir == ((i - 1) % 4):
          new_cost += 1000
        else:
          new_cost += 2000
        
        next_paths.append((new_cost, dest_pos, i, pth + [pos]))
    
    paths = sorted(next_paths, key=lambda x: x[0])

  score, pthset = best_score[target]
  #print(pthset)
  #print("\n".join("".join("#" if data[y][x] == "#" else ("O" if (x, y) in pthset else ".") for x in range(w)) for y in range(h)))
  return score, len(pthset)


#for node in nodes:
#  print(f"{node}: {graph[node]}")
#print("--")

#print(graph)
print(find_path(start, target))