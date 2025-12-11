import math

with open("data") as f:
  lines = [x for x in f if x.strip()]

ops = lines[-1] + "+"
lines = lines[:-1]
curop = ""
ns = []
total = 0
for i, c in enumerate(ops):
  if c == "*" or c == "+":
    if curop != "" and len(ns):
      #print(ns)
      if curop == "*":
        total += math.prod(ns)
      else:
        total += sum(ns)
    curop = c
    ns = []
  nstring = "".join(lines[y][i] for y in range(len(lines)))
  if nstring.strip():
    ns.append(int(nstring.strip()))
print(total)