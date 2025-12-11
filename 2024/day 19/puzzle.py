from collections import deque, defaultdict

with open("data") as f:
  parts, patterns = f.read().strip().split("\n\n")

parts = [x.strip() for x in parts.strip().split(",")]
patterns = [x.strip() for x in patterns.strip().split("\n")]

def fast_function(parts, pattern):
  position_count = defaultdict(int)
  position_count[0] = 1
  for pos in range(len(pattern) + 1):
    for part in parts:
      dest_pos = pos + len(part)
      if dest_pos <= len(pattern) and pattern[pos:dest_pos] == part:
        position_count[dest_pos] += position_count[pos]
  
  count = position_count[len(pattern)]
  return count > 0, count

total = 0 
total_count = 0
for pattern in patterns:
  result, count = fast_function(parts, pattern)
  total_count += count
  if result:
    total += 1

print(total, total_count)