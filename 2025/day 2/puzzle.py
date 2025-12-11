import math

with open("data") as f:
  data = [[int(x) for x in section.strip().split("-")] for section in f.read().strip().split(",")]

def is_duped_for_n(x, n):
  sl = len(x) // n
  if len(x) % n != 0:
    return False
  
  chunk = x[:sl]
  for i in range(1, n):
    if x[i*sl:(i+1)*sl] != chunk:
      return False
  return True

def is_duped(x):
  strx = str(x)
  for n in range(2, len(strx) + 1):
    if is_duped_for_n(strx, n):
      return True
  return False

total = 0
for start, end in data:
  for x in range(start, end+1):
    if is_duped(str(x)):
      total += x
print(total)
