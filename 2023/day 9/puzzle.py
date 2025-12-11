
def find_next(ns):
  stack = [ns]
  while any(x != 0 for x in stack[-1]):
    stack.append([stack[-1][i+1] - stack[-1][i] for i in range(len(stack[-1]) - 1)])
  
  while len(stack) > 1:
    last_val = stack.pop()[-1]
    stack[-1].append(stack[-1][-1] + last_val)
  
  return stack[-1][-1]

def find_first(ns):
  stack = [ns]
  while any(x != 0 for x in stack[-1]):
    stack.append([stack[-1][i+1] - stack[-1][i] for i in range(len(stack[-1]) - 1)])

  while len(stack) > 1:
    last_val = stack.pop()[0]
    stack[-1].insert(0, stack[-1][0] - last_val)
  
  return stack[-1][0]


with open("input") as f:
  data = [[int(x) for x in l.split()] for l in f.read().strip().split("\n")]
  total = 0 
  first_total =0
  for ns in data:
    total += find_next(ns)
    first_total += find_first(ns)
  print(total)
  print(first_total)
