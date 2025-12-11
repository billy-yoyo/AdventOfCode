
with open("data") as f:
  rangedata, iddata = f.read().strip().split("\n\n")
  ranges = [[int(x) for x in r.strip().split("-")] for r in rangedata.strip().split("\n")]
  ids = [int(x) for x in iddata.strip().split("\n")]

ranges = sorted(ranges, key=lambda x: x[0])

def pt1():
  count = 0
  for id in ids:
    for sid, eid in ranges:
      if sid > id:
        break
      elif sid <= id <= eid:
        count += 1
        break
  print(count)

def overlap(r1, r2):
  _, r1e = r1
  r2s, _ = r2
  return r2s <= r1e

new_ranges = [ranges[0]]
for r2 in ranges[1:]:
  r1 = new_ranges[-1]
  if overlap(r1, r2):
    new_ranges[-1][1] = max(r2[1], r1[1])
  else:
    new_ranges.append(r2)

total = 0
for s, e in new_ranges:
  total += (e - s) + 1

print(total)