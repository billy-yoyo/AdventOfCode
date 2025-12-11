
def report_is_safe(report):
  asc = None
  for i, x in enumerate(report[:-1]):
    if x < report[i + 1]:
      if asc is None:
        asc = True
      elif not asc:
        return False
    elif x > report[i + 1]:
      if asc is None:
        asc = False
      elif asc:
        return False
    
    gap = abs(x - report[i + 1])
    if gap < 1 or gap > 3:
      return False
  return True

with open("data") as f:
  n_safe = 0
  for line in f.read().strip().split("\n"):
    report = [int(x) for x in line.split()]
    if report_is_safe(report):
      n_safe += 1
    else:
      for i in range(len(report)):
        if report_is_safe(report[:i] + report[i + 1:]):
          n_safe += 1
          break

print(n_safe)
