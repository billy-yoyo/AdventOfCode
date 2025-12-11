import math

data = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()

with open("data") as f:
    data = f.read()

def name_to_index(name):
    return ["ore", "clay", "obsidian", "geode"].index(name)

def parse_blueprint(line):
    costs = line.split(":")[1].strip()
    costs = costs.split(".")[:-1]
    cost_map = [None, None, None, None]
    max_cost_map = [0, 0, 0, 99999]
    for cost in costs:
        name = cost.strip().split(" ")[1]
        subcosts = [x.split(" ") for x in cost.strip().split(" costs ")[1].split(" and ")]
        subcosts = [(int(amount), name_to_index(name)) for amount, name in subcosts]
        subcost_map = [0, 0, 0, 0]
        for amount, index in subcosts:
            max_cost_map[index] = max(max_cost_map[index], amount)
            subcost_map[index] = amount
    
        cost_map[name_to_index(name)] = subcost_map
    return cost_map, max_cost_map, [0]

blueprints = [parse_blueprint(line) for line in data.strip().split("\n")]

def tick_resources(robots, resources, tick_delta, building):
    return tuple((x * tick_delta) + y for x, y in zip(robots, resources))

def compute_blueprint(blueprint, ticks, robots, resources):
    #print(ticks, robots, resources)
    if ticks <= 0:
        blueprint[2][0] = max(blueprint[2][0], resources[-1])
        return resources[-1]

    max_geodes = resources[-1] + (robots[-1] * ticks)

    if max_geodes + (ticks * (ticks + 1) / 2) <= blueprint[2][0]:
        return 0

    for i in range(4):
        if robots[i] < blueprint[1][i] and all(blueprint[0][i][j] == 0 or robots[j] > 0 for j in range(4)):
            ticks_to_afford = max(0, max(0 if robots[j] == 0 else math.ceil((blueprint[0][i][j] - resources[j]) / robots[j]) for j in range(4))) + 1
            #print(f"would need to wait {ticks_to_afford} before we could afford {i}")
            if ticks >= ticks_to_afford:
                new_resources = tuple(x + (robots[j] * ticks_to_afford) - blueprint[0][i][j] for j, x in enumerate(resources))
                new_robots = tuple(x + (1 if i == j else 0) for j, x in enumerate(robots))
                max_geodes = max(max_geodes, compute_blueprint(blueprint, ticks - ticks_to_afford, new_robots, new_resources))
    return max_geodes

blueprints = blueprints[:3]

times = [compute_blueprint(b, 32, (1, 0, 0, 0), (0, 0, 0, 0)) for b in blueprints]
print(times)
print(times[0] * times[1] * times[2])




    

