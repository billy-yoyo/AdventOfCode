from functools import cache
from collections import defaultdict

def mix(x, y):
  return x ^ y

def prune(x):
  return x % 16777216

def step_secret(x):
  x = prune(mix(x * 64, x))
  x = prune(mix(x // 32, x))
  x = prune(mix(x * 2048, x))
  return x

def nth_secret(x, n):
  for _ in range(n):
    x = step_secret(x)
  return x

def best_seq(init_xs, n):
  counts = defaultdict(list)
  
  for xi, x in enumerate(init_xs):
    sub_counts = {}
    last_seq = (None, None, None, None)
    last_dig = x % 10
    for ni in range(n-1):
      x = step_secret(x)
      digit = x % 10
      dx = digit - last_dig

      last_seq = last_seq[1:] + (dx,)
      if None not in last_seq and last_seq not in sub_counts:
        sub_counts[last_seq] = digit
      last_dig = digit
    
    for k, v in sub_counts.items():
      counts[k].append(v)
  
  #print(counts[(-2,1,-1,3)])
  seq, count = max(counts.items(), key=lambda x: sum(x[1]))
  print(seq)
  print(count)
  return sum(count)

with open("data") as f:
  nums = [int(x) for x in f.read().strip().split("\n")]

total = sum(nth_secret(n, 2000) for n in nums)
print(total)

print(best_seq(nums, 2000))

