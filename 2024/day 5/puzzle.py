
with open("data") as f:
  rules, data = f.read().strip().split("\n\n")

rules = [[int(x) for x in rule.split("|")] for rule in rules.strip().split("\n")]
data = [[int(x) for x in line.split(",")] for line in data.strip().split("\n")]

total = 0
for ns in data:
  for x, y in rules:
    if x in ns and y in ns and ns.index(x) > ns.index(y):
      break
  else:
    total += ns[len(ns) // 2]

def attempt_order(ns, rules):
  changed = False
  for x, y in rules:
    if x not in ns or y not in ns:
      continue
    
    xi = ns.index(x)
    yi = ns.index(y)

    if xi > yi:
      ns[xi], ns[yi] = y, x
      changed = True
  return changed

total_2 = 0
for ns in data:
  iterations = 0
  while attempt_order(ns, rules):
    iterations += 1
    pass
  if iterations >= 1:
    total_2 += ns[len(ns) // 2]


print(total)
print(total_2)


