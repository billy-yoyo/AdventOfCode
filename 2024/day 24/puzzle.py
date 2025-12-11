from collections import defaultdict, deque
from functools import cache
from itertools import combinations
import re

def setreg(regs, key, value):
  regs[key] = value
  return key

gates = {
  "AND": lambda a,b: a & b,
  "OR": lambda a,b: a | b,
  "XOR": lambda a,b: a ^ b,
}

zkeys = []
inner_keys = []
calcs = {}

def compile(line):
  op, out = line.strip().split("->")
  a, cmd, b = op.strip().split(" ")

  out = out.strip()

  if out.startswith("z"):
    zkeys.append(out)

  inner_keys.append(out)

  if out in calcs:
    raise Exception(f"multiple outputs for {out}")
  
  calcs[out] = (cmd, a, b)

regs = {}
queue = deque([])

with open("data") as f:
  inits, code = f.read().strip().split("\n\n")
  for init in inits.strip().split("\n"):
    name, val = init.strip().split(":")
    regs[name.strip()] = int(val.strip())
    queue.append(name.strip())

  for line in code.strip().split("\n"):
    compile(line)

@cache
def eval(name):
  if name in regs:
    return regs[name]
  elif name in calcs:
    cmd, a, b = calcs[name]
    return gates[cmd](eval(a), eval(b)) 
  else:
    raise Exception(f"cannot evaluate {name}")
  
testcases = []

for i in range(1, 46):
  for j in range(i):
    testcases.append(("0" * j) + ("1" * (i - j)) + ("0" * (45 - i)))

# z02 = f ^ ^02
# z03 = ((f & ^02) | &02) ^ ^03

bitcom = re.compile(r"(?:\^|\&)([0-9]+)")

cmd_codemap = {"AND":"&","OR":"|","XOR":"^"}

@cache
def stringify(name):
  if name.startswith("x") or name.startswith("y"):
    return name
  elif name in calcs:
    cmd, a, b = calcs[name]
    if {a[0], b[0]} == set("xy") and a[1:] == b[1:]:
      return f"{cmd_codemap[cmd]}{a[1:]}"
    
    sa, sb = stringify(a), stringify(b)
    a_lowest = None
    b_lowest = None
  
    for match in bitcom.findall(sa):
      match = int(match)
      if a_lowest is None or match < a_lowest:
        a_lowest = match
    
    for match in bitcom.findall(sb):
      match = int(match)
      if b_lowest is None or match < b_lowest:
        b_lowest = match

    if a_lowest < b_lowest:
      return f"({stringify(a)} {cmd_codemap[cmd]} {stringify(b)})"
    else:
      return f"({stringify(b)} {cmd_codemap[cmd]} {stringify(a)})"
  else:
    raise Exception(f"cannot evaluate {name}")

@cache
def expected_stringify(zkey):
  n = int(zkey[1:])
  if n == 0:
    return "^00"
  if n == 1:
    return "(&00 ^ ^01)"

  pn = n - 1
  pzkey = f"z0{pn}" if pn < 10 else f"z{pn}"
  prev = expected_stringify(pzkey)
  prev_end = prev[-3:-1]
  prev_start = prev[1:-7]

  s = f"({prev_start} & ^{prev_end})"
  s = f"({s} | &{prev_end})"
  return f"({s} ^ ^{zkey[1:]})"

def swap_pairs(pairs):
  for a, b in pairs:
    calcs[a], calcs[b] = calcs[b], calcs[a]
  stringify.cache_clear()


def test_pairs(pairs):
  swap_pairs(pairs)
  
  try:
    for zkey in zkeys:
      if stringify(zkey) != expected_stringify(zkey):
        return int(zkey[1:])
  except:
    return 0
  finally:
    swap_pairs(pairs)

  return None

def outs_for_key(key):
  if key in calcs:
    _, a, b = calcs[key]
    return outs_for_key(a) | outs_for_key(b) | {key,}
  else:
    return {key,}

def outs_before_zkey(pairs, zkey):
  swap_pairs(pairs)
  outs = set()
  for i in range(zkey):
    key = f"z0{i}" if i < 10 else f"z{i}"
    outs |= outs_for_key(key)
  swap_pairs(pairs)
  return outs

zkeys = sorted(zkeys)

def main():
  zbits = []
  for zkey in zkeys:
    sz, esz = stringify(zkey), expected_stringify(zkey)

    if sz == esz:
      print(f"{zkey}: OK")
    else:
      print(f"{zkey}: [{sz}] != [{esz}]")

    zbits.append(eval(zkey))
  zbits = zbits[::-1]

  print(zbits)
  z = int("".join([str(x) for x in zbits]), 2)
  print(z)


def pair_find():
  pairs = []
  while len(pairs) < 4:
    print(pairs)
    zkey = test_pairs(pairs)
    if not zkey:
      break

    valid_keys = set(inner_keys) - outs_before_zkey(pairs, zkey)
    for pair in combinations(valid_keys, 2):
      if test_pairs(pairs + [pair]) > zkey:
        pairs.append(pair)
        break
    else:
      for pair1 in combinations(valid_keys, 2):
        for pair2 in combinations(valid_keys, 2):
          if test_pairs(pairs + [pair1, pair2]) > zkey:
            pairs.append(pair1)
            pairs.append(pair2)
            break
        else:
          continue
        break

  return pairs

pairs = pair_find()
final_keys = []
for a, b in pairs:
  final_keys.append(a)
  final_keys.append(b)

print(",".join(sorted(final_keys)))

#swap_pairs(pairs)
#main()

