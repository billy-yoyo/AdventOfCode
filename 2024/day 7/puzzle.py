from itertools import product

with open("data") as f:
  data = [x.strip().split(": ") for x in f.read().strip().split("\n")]

operators = [
  lambda a,b: a+b,
  lambda a,b: a*b,
  lambda a,b: int(str(a)+str(b))
]

def evaluate(ns, opis):
  x = ns[0]
  for opi, y in zip(opis, ns[1:]):
    x = operators[opi](x, y)
  return x

def can_hit_target(target, ns):
  for opis in product(range(len(operators)), repeat=len(ns) - 1):
    if evaluate(ns, opis) == target:
      return True
  return False

total = 0
for target, s in data:
  target = int(target)
  ns = [int(x) for x in s.split(" ")]
  if can_hit_target(target, ns):
    total += target

print(total)

