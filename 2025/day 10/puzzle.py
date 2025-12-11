from itertools import combinations

with open("data") as f:
  parts = []
  for line in f:
    line_parts = line.strip().split(" ")
    lights_string, buttons_string, joltage_string = line_parts[0], line_parts[1:-1], line_parts[-1]
    lights_target = [1 if x == "#" else 0 for x in lights_string[1:-1]]
    buttons = [[int(x) for x in b[1:-1].split(",")] for b in buttons_string]
    joltage = [int(x) for x in joltage_string[1:-1].split(",")]
    parts.append((lights_target, buttons, joltage))

def solve_with(target, eqns, states):
  eqns_state = eqns_with_states(eqns, states)

  # every button has been pressed for a specific target, and the value is wrong
  if any(len(bs) == 0 and value != target[t] for t, bs, value in eqns_state):
    return -1
  
  if all(value == target[t] for t, _, value in eqns_state):
    #print(states)
    return sum(1 for _, state in states.items() if state)

  t, bs, value = next(x for x in eqns_state if len(x[1]) > 0)
  if len(bs) == 1:
    new_states = dict(states)
    new_states[bs[0]] = 0 if value == target[t] else 1
    return solve_with(target, eqns, new_states)
  else:
    required_state = 0 if value == target[t] else 1
    best_soln = -1
    for w in range(required_state, len(bs) + 1, 2):
      for sub_bs in combinations(bs, w):
        new_states = dict(states)
        for b in bs:
          new_states[b] = 1 if b in sub_bs else 0
        soln = solve_with(target, eqns, new_states)
        if soln > 0 and (best_soln < 0 or soln < best_soln):
          best_soln = soln
    return best_soln



def eqns_with_states(eqns, states):
  return sorted([(t, [b for b in buttons if b not in states], (sum(states[b] for b in buttons if b in states)) % 2) for t, buttons, _ in eqns], key=lambda x: len(x[1]))

total = 0
for i, (target, buttons, _) in enumerate(parts):
  equations = [(t, [i for i, b in enumerate(buttons) if t in b], 0) for t, _ in enumerate(target)]
  equations = sorted(equations, key=lambda x: len(x[1]))

  states = {}
  for t, bs, value in equations:
    if len(bs) == 1:
      states[bs[0]] = target[t]
    else:
      break
  
  soln = solve_with(target, equations, states)
  if soln == -1:
    print(f"failed to find solution for [{i}] {target} {buttons}")
  total += soln

print(total)

