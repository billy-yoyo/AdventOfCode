
with open("data") as f:
  cols = None
  for line in f.read().strip().split("\n"):
    cells = line.split()
    if cols is None:
      cols = [[] for _ in cells]
    for cell, col in zip(cells, cols):
      col.append(int(cell))
  
cols = [sorted(col) for col in cols]

a, b = cols[0], cols[1]
total = sum(abs(x - y) for x, y in zip(a, b))
print(total)

total_2 = sum(x * b.count(x) for x in a)
print(total_2)
