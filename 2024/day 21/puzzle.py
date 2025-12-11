from functools import cache
from itertools import product, chain

numpad = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", "A"]
dirpad = ["^", "A", "<", "v", ">"]

numpad_map = [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2),(1,3),(2,3)]
dirpad_map = [(1,0),(2,0),(0,1),(1,1),(2,1)]
dirpad_off_map = [(0,-1),None,(-1,0),(0,1),(1,0)]

offs = [(0,1),(0,-1),(1,0),(-1,0)]
def get_paths(from_pos, to_pos, positions):
  paths = []
  stack = [[from_pos]]
  while stack:
    next_stack = []
    for path in stack:
      x, y = path[-1]
      if (x, y) == to_pos:
        paths.append(path)
        continue
      for ox, oy in offs:
        nx, ny = x + ox, y + oy
        if (nx, ny) in positions and (nx, ny) not in path:
          next_stack.append(path + [(nx, ny)])
    stack = next_stack

  if paths:
    min_length = min(len(p) for p in paths)
    paths = [[(p[i+1][0] - x, p[i+1][1] - y) for i, (x, y) in enumerate(p[:-1])] for p in paths if len(p) == min_length]

  return paths

def get_pad_paths(from_val, to_val, pad, pad_map):
  i1, i2 = pad.index(from_val), pad.index(to_val)
  p1, p2 = pad_map[i1], pad_map[i2]
  dpad_chars = [[dirpad[dirpad_off_map.index(p)] for p in path] + ["A"] for path in get_paths(p1, p2, pad_map)]

  # count repeating
  any_repeating = any(any(c[i] == c[i+1] for i in range(len(c) - 1)) for c in dpad_chars)
  if any_repeating:
    dpad_chars = [c for c in dpad_chars if any(c[i] == c[i+1] for i in range(len(c) - 1))]
  
  return dpad_chars

@cache
def get_numpad_paths(from_val, to_val):
  return get_pad_paths(from_val, to_val, numpad, numpad_map)

@cache
def get_dirpad_paths(from_val, to_val):
  return get_pad_paths(from_val, to_val, dirpad, dirpad_map)
  

@cache
def expand(chars, levels):
  if levels == 0:
    return len(chars)

  all_paths = [get_dirpad_paths(chars[i], chars[i+1]) for i in range(len(chars) - 1)]
  all_paths.insert(0, get_dirpad_paths("A", chars[0]))

  size = 0
  for paths in all_paths:
    size += min(expand("".join(path), levels - 1) for path in paths)

  return size

def calc(code):
  size = 0
  value = "A"
  for c in code:
    best_sub_size = None
    for path in get_numpad_paths(value, c):
      sub_size = expand("".join(path), 25)
      if best_sub_size is None or sub_size < best_sub_size:
        best_sub_size = sub_size
    size += best_sub_size
    value = c
  return size

example = ["029A", "980A", "179A", "456A", "379A"]
data = ["169A", "279A", "540A", "869A", "789A"]

total = 0
for code in data:
  size = calc(code)
  print(f"{code} = {size} * {int(code[:-1])}")
  total += size * int(code[:-1])

print(total)
