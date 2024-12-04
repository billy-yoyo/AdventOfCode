import re

pattern = re.compile(r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))")

with open("data") as f:
  data = f.read().strip()

total = 0
enabled = True
for is_mul, x, y, is_do, is_dont in pattern.findall(data):
  if is_mul:
    if enabled:
      total += int(x) * int(y)
  elif is_do:
    enabled = True
  elif is_dont:
    enabled = False

print(total)
