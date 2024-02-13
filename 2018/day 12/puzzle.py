from collections import defaultdict

with open("input") as f:
    first, rest = f.read().strip().split("\n\n")

initial_state = first.split(":")[1].strip()

transformer = defaultdict(lambda: ".")
for line in rest.strip().split("\n"):
    state, target = line.split("=>")
    transformer[state.strip()] = target.strip()

def count_at_start(x, c):
    i = 0
    while x[i] == c:
        i += 1
    return i

def gen_next_state(state):
    state = "...." + state + "...."
    next_state = list(state)
    for i, _ in enumerate(state):
        local = state[max(0, i-2):i+3]
        if i < 2:
            local = ("." * (5 - len(local))) + local
        elif i >= len(state) - 2:
            local += "." * (5 - len(local))
        next_state[i] = transformer[local]
    next_state = "".join(next_state)
    header = count_at_start(next_state, ".")
    return next_state.strip("."), header - 4

def get_pots_after(steps, inital_offset):
    state, start_offset = initial_state, inital_offset
    for _ in range(steps):
        state, offset = gen_next_state(state)
        start_offset += offset
    return sum(x + start_offset for x, c in enumerate(state) if c == "#")

def get_offset_and_period():
    visited = {}

    state, start_offset = initial_state, 0
    i = 0
    while True:
        if state in visited:
            first_visit, old_offset = visited[state]
            return first_visit, i - first_visit, start_offset - old_offset
        visited[state] = (i, start_offset)
        state, offset = gen_next_state(state)
        start_offset += offset
        i += 1

gens = 50000000000
offset, period, offset_diff = get_offset_and_period()        
print(f"found {offset=} {period=} {offset_diff=}")
steps = (gens - offset) % period
offset_diff = ((gens - offset) // period) * offset_diff

print(get_pots_after(offset + steps, offset_diff))
