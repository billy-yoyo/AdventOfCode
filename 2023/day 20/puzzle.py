from collections import defaultdict
import math

LOW = 1
HIGH = 2

flip_flop_times = {}

def create_flipflop(name, destinations):
    state = [False]
    def recv(source, x):
        if x == LOW:
            next_pulse = LOW if state[0] else HIGH
            state[0] = not state[0]
            return [(name, next_pulse, dest) for dest in destinations]
        else:
            return []
    return recv

def create_conjunction(name, destinations, inputs):
    state = {i: LOW for i in inputs}
    if "rx" not in destinations:
        flip_flop_times[name] = None
    def recv(source, x):
        state[source] = x
        next_pulse = LOW if all(v == HIGH for v in state.values()) else HIGH
        if name in flip_flop_times and flip_flop_times[name] is None and next_pulse == LOW:
            flip_flop_times[name] = presses + 1
        return [(name, next_pulse, dest) for dest in destinations]
    return recv

def create_broadcaster(destinations):
    def recv(source, x):
        return [("broadcaster", x, dest) for dest in destinations]
    return recv

with open("input") as f:
    lines = f.read().strip().split("\n")
    all_names = [x[1:] if x[0] in "&%" else x for x in [l.split(" -> ")[0].strip() for l in lines]]
    all_destinations = [l.split(" -> ")[1].strip().split(", ") for l in lines]
    all_inputs = [[input_name for i, input_name in enumerate(all_names) if name in all_destinations[i]] for name in all_names]
    all_functypes = [l.strip()[0] for l in lines]

    function_info = { name: (dests, inputs, functype) for name, dests, inputs, functype in zip(all_names, all_destinations, all_inputs, all_functypes) }
    
    functions = {}

    for i, line in enumerate(lines):
        name, destinations = line.split(" -> ")
        name = name.strip()
        destinations = destinations.strip().split(", ")
        if name.startswith("%"):
            name = name[1:]
            receiver = create_flipflop(name, destinations)
        elif name.startswith("&"):
            name = name[1:]
            inputs = [input_name for i, input_name in enumerate(all_names) if name in all_destinations[i]]
            receiver = create_conjunction(name, destinations, inputs)
        elif name == "broadcaster":
            receiver = create_broadcaster(destinations)
        else:
            raise Exception(f"Invalid name {name}")
        functions[name] = receiver


def press_button(functions):
    counts = defaultdict(int)
    state = [("button", LOW, "broadcaster")]
    for source, x, destination in state:
        counts[x] += 1
        if destination in functions:
            for new_entry in functions[destination](source, x):
                state.append(new_entry)
    return counts

lows, highs = 0, 0
presses = 0
while True:
    counts = press_button(functions)
    presses += 1
    lows += counts[LOW]
    highs += counts[HIGH]
    if presses == 1000:
        # part 1
        print(lows * highs)
    
    if all(v is not None for v in flip_flop_times.values()):
        break

# part 2
answer = 1
for v in flip_flop_times.values():
    answer = math.lcm(answer, v)
print(answer)
