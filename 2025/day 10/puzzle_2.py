

with open("data") as f:
  parts = []
  for line in f:
    line_parts = line.strip().split(" ")
    lights_string, buttons_string, joltage_string = line_parts[0], line_parts[1:-1], line_parts[-1]
    lights_target = [1 if x == "#" else 0 for x in lights_string[1:-1]]
    buttons = [[int(x) for x in b[1:-1].split(",")] for b in buttons_string]
    joltage = [int(x) for x in joltage_string[1:-1].split(",")]
    parts.append((lights_target, buttons, joltage))

def solve_with(eqns, states, bound=0):
  eqns_state = eqns_with_states(eqns, states)
  reduce_eqns(eqns_state)
  #print(eqns_state)
  #print(states)

  if bound > 0 and sum(state for state in states.values()) >= bound:
    return -1

  # every button has been pressed for a specific target, and the value is wrong
  if any((len(bs) == 0 and value != t) or value > t for t, bs, value in eqns_state):
    return -1
  
  if all(value == t for t, _, value in eqns_state):
    return sum(state for _, state in states.items())


  t, bs, value = next(x for x in eqns_state if len(x[1]) > 0)
  if len(bs) == 1:
    new_states = dict(states)
    for t, bs, value in eqns_state:
      if len(bs) > 1:
        break
      elif len(bs) == 1:
        new_states[bs[0]] = t - value
    
    return solve_with(eqns, new_states)

  best_soln = -1
  for v in range(0, 1 + t - value):
    new_states = dict(states)
    new_states[bs[0]] = v
    soln = solve_with(eqns, new_states, bound=best_soln)
    if soln > 0 and (best_soln < 0 or soln < best_soln):
      best_soln = soln

  return best_soln

def eqns_with_states(eqns, states):
  return sorted([(t, [b for b in buttons if b not in states], (sum(states[b] for b in buttons if b in states))) for t, buttons, _ in eqns], key=lambda x: len(x[1]))

def reduce_eqns(eqns):
  reduced = False
  for i, (t, bs, v) in enumerate(eqns):
    if len(bs) == 0:
      continue
    new_bs = list(bs)
    for j in range(i):
      t2, bs2, v2 = eqns[j]
      if len(bs2) == 0:
        continue
      if all(b in new_bs for b in bs2):
        reduced = True
        #print(f"subtracting {bs2} from {bs}")
        for b in bs2:
          new_bs.remove(b)
        t -= t2 - v2
    eqns[i] = (t, new_bs, v)
  return reduced

total = 0
for i, (_, buttons, target) in enumerate(parts):
  print(f"{i * 100 / len(parts):.2f}% done")
  equations = [(tv, [i for i, b in enumerate(buttons) if t in b], 0) for t, tv in enumerate(target)]
  equations = sorted(equations, key=lambda x: len(x[1]))

  states = {}
  for t, bs, value in equations:
    if len(bs) == 1:
      states[bs[0]] = t
    else:
      break
  
  soln = solve_with(equations, states)
  if soln == -1:
    print(f"failed to find solution for [{i}] {target} {buttons}")
  total += soln


print(total)

