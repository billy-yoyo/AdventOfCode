from functools import cache
import time

@cache
def split_n(x):
  strx = str(x)
  if len(strx) % 2 == 0:
    lenx = len(strx) // 2
    return int(strx[:lenx]), int(strx[lenx:])
  return (x*2024,)

@cache
def num_stones(x, iters):
  if iters == 0:
    return 1

  if x == 0:
    return num_stones(1, iters - 1)
  
  total = 0
  for subx in split_n(x):
    total += num_stones(subx, iters - 1)
  return total

example = [125, 17]
data = [27, 10647, 103, 9, 0, 5524, 4594227, 902936]

start = time.time()
total = 0
for start_stone in data:
  total += num_stones(start_stone, 75)

print(total)
print(time.time() - start)


