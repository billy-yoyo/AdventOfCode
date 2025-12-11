import re
import math

with open("example") as f:
  lines = [re.split(r"\s+", x.strip()) for x in f if x.strip()]

width = len(lines[0])
cols = [
  [lines[y][x] for y in range(len(lines))] for x in range(width)
]



total = 0
for col in cols:
  nums, op = [int(x) for x in col[:-1]], col[-1]
  if op == "*":
    total += math.prod(nums)
  else:
    total += sum(nums)
print(total)

