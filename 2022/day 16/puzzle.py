
data = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()

with open("data") as f:
    data = f.read()

def parse_valve(line):
    left, right = line.split("; ")
    valve_left, rate = left.split("=")
    valve_name = valve_left.split(" ")[1]
    valve_rate = int(rate)
    connections = " ".join(right.split(" ")[4:]).split(", ")
    return (valve_name, valve_rate, connections)

valves = {}

for line in data.split("\n"):
    name, rate, conns = parse_valve(line)
    valves[name] = (rate, conns)

valve_full_cons = {}

for valve, (rate, conns) in [(v, rc) for v, rc in valves.items() if v == "AA" or rc[0] > 0]:
    valve_full_cons[valve] = { c: 1 for c in conns }
    full_cons = valve_full_cons[valve]
    stack = [(c, 1) for c in conns]
    while stack:
        new_stack = []
        for dest, length in stack:
            dest_conns = valves[dest][1]
            for new_dest in dest_conns:
                if new_dest not in full_cons:
                    full_cons[new_dest] = length + 1
                    new_stack.append((new_dest, length + 1))
        stack = new_stack

def find_best_path(visited, time, pressure):
    location = visited[-1]
    unvisited = (set(valve_full_cons) - set(visited))
    if unvisited == 0:
        yield pressure
        return

    if time <= 1:
        yield pressure
        return
    
    found_valid = False
    for new_location in unvisited:
        time_cost = valve_full_cons[location][new_location] + 1
        new_time = time - time_cost
        if new_time >= 0:
            found_valid = True
            new_pressure = pressure + (valves[new_location][0] * new_time)
            yield from find_best_path(visited + [new_location], new_time, new_pressure)

    if not found_valid:
        yield pressure

best_pressure = max(find_best_path(["AA"], 30, 0))
print(best_pressure)
