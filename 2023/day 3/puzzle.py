from collections import defaultdict

with open("input") as f:
  lines = [x.strip() for x in f.readlines() if x.strip()]


digits = "0123456789"
non_special = "0123456789."

adjs = defaultdict(list)

def any_adjacent(y, x0, x1, n):
  is_adj = False
  if x0 > 0 and lines[y][x0-1] not in non_special:
    is_adj = True
    adjs[(x0-1, y)] += [n]
  if x1 < len(lines[y]) and lines[y][x1] not in non_special:
    is_adj = True
    adjs[(x1, y)] += [n]    
  if y > 0:
    for x in range(max(0, x0-1), min(len(lines[y-1]), x1+1)):
      if lines[y-1][x] not in non_special:
        is_adj = True
        adjs[(x, y-1)] += [n]
  if y < len(lines) - 1:
    for x in range(max(0, x0-1), min(len(lines[y+1]), x1+1)):
      if lines[y+1][x] not in non_special:
        is_adj = True
        adjs[(x, y+1)] += [n]
  
  return is_adj

total = 0

for y, line in enumerate(lines):
  start = -1
  for x, c in enumerate(line):
    if c in digits:
      if start == -1:
        start = x
    elif start >= 0:
      n = int(line[start:x])
      if any_adjacent(y, start, x, n):
        #print(f"({start}:{x}, {y}) {line[start:x]} is adjacent")
        total += n
      start = -1
    
  if start >= 0:
    n = int(line[start:])
    if any_adjacent(y, start, len(line), n):
    #print(f"({start}:{len(line)}, {y}) {line[start]} is adjacent")
      total += n

print(total)

second_total = 0
for (x, y), ns in adjs.items():
  if lines[y][x] == "*" and len(ns) == 2:
    second_total += ns[0] * ns[1]

print(second_total)