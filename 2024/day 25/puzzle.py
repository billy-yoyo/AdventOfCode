
locks = []
keys = []

total_height = 0
with open("data") as f:
  for block in f.read().strip().split("\n\n"):
    block = block.strip().split("\n")
    total_height = len(block)
    lowest = []
    heighest = []
    for x in range(len(block[0])):
      for y in range(len(block)):
        if block[y][x] == "#":
          lowest.append(len(block) - (y + 1))
          break
      
      for y in range(len(block) - 1, -1, -1):
        if block[y][x] == "#":
          heighest.append(y)
          break

    if block[0][0] == "#":
      locks.append(heighest)
    else:
      keys.append(lowest)

count = 0
for lock in locks:
  for key in keys:
    if all(x + y < total_height - 1 for x, y in zip(lock, key)):
      count += 1

print(count)