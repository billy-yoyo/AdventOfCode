from collections import defaultdict

with open("data") as f:
  coords = [[int(x) for x in l.strip().split(",")] for l in f if l.strip()]

def rect_area(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  dx = 1 + max(x1, x2) - min(x1, x2)
  dy = 1 + max(y1, y2) - min(y1, y2)
  return dx * dy

horz_pairs = []
vert_pairs = []

for i, p in enumerate(coords[:-1]):
  before = (i - 1) % len(coords)
  after = (i + 1) % len(coords)
  
  bp = coords[before]
  ap = coords[after]

  if p[0] == bp[0]:
    vert_pairs.append((i, before))
  else:
    horz_pairs.append((i, before))

  if p[0] == ap[0]:
    vert_pairs.append((i, after))
  else:
    horz_pairs.append((i, after))

horz_pairs = sorted(horz_pairs, key=lambda x: coords[x[0]][1])
horz_pairs = [
  (min(coords[i][0], coords[j][0]), max(coords[i][0], coords[j][0]), coords[i][1]) for i, j in horz_pairs
]

vert_pairs = sorted(vert_pairs, key=lambda x: coords[x[0]][0])
vert_pairs = [
  (min(coords[i][1], coords[j][1]), max(coords[i][1], coords[j][1]), coords[i][0]) for i, j in vert_pairs
]

def is_yrange_free(x1, x2, y1, y2):
  for s, e, x in vert_pairs:
    if x <= x1:
      continue
    elif x >= x2:
      break
    
    if y1 + 1 <= e and s <= y2 - 1:
      return False
  return True



best_2 = 0
for i, (s1, e1, y1) in enumerate(horz_pairs):
  for j in range(i):
    (s2, e2, y2) = horz_pairs[j]

    x1, x2 = min(s1, s2), max(e1, e2)

    for k in range(j + 1, i):
      ks, ke, _ = horz_pairs[k]
      if ks <= x1 and ke > x1:
        if x1 == min(s1, s2) and ke <= max(s1, s2):
          x1 = max(s1, s2)
        else:
          x1, x2 = 0, 0
          break
      elif ks < x2 and ke >= x2:
        if x2 == max(e1, e2) and ks >= min(e1, e2):
          x2 = max(e1, e2)
        else:
          x1, x2 = 0, 0
          break
      elif x1 < ks and ke < x2:
        x1, x2 = 0, 0
        break
      elif ks <= x1 and x2 <= ke:
        x1, x2 = 0, 0
        break

    
    if (x1 != 0 or x2 != 0) and is_yrange_free(x1, x2, y2, y1):
      area = (1 + x2 - x1) * (1 + y1 - y2)
      #print(f"found xrange {(x1, x2)} = {area}")
      if area > best_2:
        best_2 = area


best = 0
for i in range(len(coords)):
  for j in range(i):
    area = rect_area(coords[i], coords[j])
    if area > best:
      best = area
print(best)
print(best_2)