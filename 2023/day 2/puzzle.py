from collections import defaultdict

def read_colours(draw):
  return {colour: int(n) for n, colour in [x.strip().split(" ") for x in draw.split(",")]}

def read_all_colours(line):
  combined = defaultdict(int)
  all_dicts = [read_colours(x) for x in line.split(":")[1].strip().split(";")]
  for a_dict in all_dicts:
    for x, n in a_dict.items():
      combined[x] = max(combined[x], n)
  return combined
  

total = 0
with open("input") as f:
  for i, line in enumerate(f):
    if line.strip():
      colours = read_all_colours(line)
      total += colours["red"] * colours["green"] * colours["blue"]
      #if colours["red"] <= 12 and colours["green"] <= 13 and colours["blue"] <= 14:
      #  total += i + 1

print(total)