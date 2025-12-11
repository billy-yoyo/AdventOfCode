from timeit import timeit

with open("data") as f:
  lines = [[int(x) for x in line.strip()] for line in f if line.strip()]

def find_best(line, size):
  stack = [-1] * size
  for j, n in enumerate(line):
    for i, on in enumerate(stack):
      from_end = len(line) - j
      if from_end < size and i < size - from_end:
        continue

      if n > on:
        stack[i] = n
        for oi in range(i + 1, size):
          stack[oi] = -1
        break
  best = 0
  for i, n in enumerate(stack):
    best += n * (10 ** (size - (i + 1)))
  return best

def run():
  total = 0
  for line in lines:
    best = find_best(line, 12)
    total += best

print(timeit(run, number=1000) / 1000)