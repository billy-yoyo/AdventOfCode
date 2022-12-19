import math

data = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()

#with open("data") as f:
#    data = f.read()

def parse_blueprint(line):
    costs = line.split(":")[1].strip()
    costs = costs.split(".")[:-1]
    cost_map = {}
    max_cost_map = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 9999999}
    for cost in costs:
        name = cost.strip().split(" ")[1]
        subcosts = [x.split(" ") for x in cost.strip().split(" costs ")[1].split(" and ")]
        subcosts = [(int(amount), name) for amount, name in subcosts]
        subcost_map = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        for amount, subcostname in subcosts:
            max_cost_map[subcostname] = max(max_cost_map[subcostname], amount)
            subcost_map[subcostname] = amount
    
        cost_map[name] = subcost_map
    return cost_map, max_cost_map

blueprints = [parse_blueprint(line) for line in data.strip().split("\n")]


def ri(resource):
    if resource == "ore":
        return 0
    elif resource == "clay":
        return 1
    elif resource == "obsidian":
        return 2
    else:
        return 3

def rn(index):
    return ["ore", "clay", "obsidian", "geode"][index]

def can_afford(blueprint, resources, resource):
    return all(resources[ri(name)] >= amount for name, amount in blueprint[0][resource].items())

def evaluate_bluepint(blueprint, time, robots, resources):
    # cull obviously bad paths
    if time < 3 and robots[-1] == 0:
        return

    affordable = [r for r in blueprint[0] if robots[ri(r)] < blueprint[1][r] and can_afford(blueprint, resources, r)]
    
    if time > 0:
        time -= 1
        resources = tuple(x + robots[i] for i, x in enumerate(resources))
    
    if time <= 0:
        #print(time, robots, resources)
        yield resources[3]
        return
    
    for r in affordable:
        new_robots = tuple(x + (1 if i == ri(r) else 0) for i, x in enumerate(robots))
        new_resources = tuple(x - blueprint[0][r][rn(i)] for i, x in enumerate(resources))
        
        yield from evaluate_bluepint(blueprint, time, new_robots, new_resources)
    
    yield from evaluate_bluepint(blueprint, time, robots, resources)

def evaluate_blueprint_2(blueprint, time, robots, resources):
    affordable = get_affordable(blueprint, robots, resources)

    while time > 0 and not affordable:
        for i, x in enumerate(robots):
            resources[i] += x
        time -= 1
        affordable = get_affordable(blueprint, robots, resources)
    
    #print(time, robots, resources, affordable)
    
    if time <= 0:
        return resources[-1]

    if time < 3 and robots[-1] == 0:
        return 0

    time -= 1
    for i, x in enumerate(robots):
        resources[i] += x

    max_geodes = 0
    for r in affordable:
        build(blueprint, robots, resources, r)
        max_geodes = max(max_geodes, evaluate_blueprint_2(blueprint, time, robots, resources))
        unbuild(blueprint, robots, resources, r)

    max_geodes = max(max_geodes, evaluate_blueprint_2(blueprint, time, robots, resources))

    for i, x in enumerate(robots):
        resources[i] -= x

    return max_geodes


def get_affordable(blueprint, robots, resources):
    return [r for r in blueprint[0] if robots[ri(r)] < blueprint[1][r] and can_afford(blueprint, resources, r)]

def build(blueprint, robots, resources, resource):
    robots[ri(resource)] += 1
    for subr in blueprint[0][resource]:
        resources[ri(subr)] -= blueprint[0][resource][subr]

def unbuild(blueprint, robots, resources, resource):
    robots[ri(resource)] -= 1
    for subr in blueprint[0][resource]:
        resources[ri(subr)] += blueprint[0][resource][subr]


def compute_blueprint(blueprint, time, robots, resources):
    if time <= 0:
        return resources[-1]

    to_build = None

    # first we need a clay robot
    if robots[1] == 0:
        if can_afford(blueprint, resources, "clay"):
            to_build = "clay"
        else:
            turns_with_none = math.ceil((blueprint[0]["clay"]["ore"] - (resources[0] + robots[0])) / robots[0])
            turns_with_ore = math.ceil((blueprint[0]["clay"]["ore"] + blueprint[0]["clay"]["ore"] - (resources[0] + robots[0])) / robots[0])
            
            if can_afford(blueprint, resources, "ore") and turns_with_ore <= turns_with_ore:
                to_build = "ore"
            else:
                to_build = None

    # second we want to try and make a obsidian robot
    elif robots[2] == 0:
        # can we afford it already
        if can_afford(blueprint, resources, "obsidian"):
            to_build = "obsidian"
        # choose build to optimize getting obsidian as soon as possible
        else:
            turns_with_none = max(
                math.ceil((blueprint[0]["obsidian"]["ore"] - (resources[0] + robots[0])) / robots[0]),
                math.ceil((blueprint[0]["obsidian"]["clay"] - (resources[1] + robots[1])) / robots[1])
            )

            turns_with_ore = max(
                math.ceil((blueprint[0]["obsidian"]["ore"] + blueprint[0]["ore"]["ore"] - (resources[0] + robots[0])) / (robots[0] + 1)),
                math.ceil((blueprint[0]["obsidian"]["clay"] + blueprint[0]["ore"]["clay"] - (resources[1] + robots[1])) / robots[1])
            )

            turns_with_clay = max(
                math.ceil((blueprint[0]["obsidian"]["ore"] + blueprint[0]["clay"]["ore"] - (resources[0] + robots[0])) / robots[0]),
                math.ceil((blueprint[0]["obsidian"]["clay"] + blueprint[0]["clay"]["clay"]- (resources[1] + robots[1])) / (robots[1] + 1))
            )

            if can_afford(blueprint, resources, "clay") and turns_with_clay <= turns_with_none and turns_with_clay <= turns_with_ore:
                to_build = "clay"
            elif can_afford(blueprint, resources, "ore") and turns_with_ore <= turns_with_none:
                to_build = "ore"
            else:
                to_build = None
    # third we want to try and make a geode robot
    elif robots[3] == 0:
        # can we afford it already
        if can_afford(blueprint, resources, "geode"):
            to_build = "geode"
        # choose build to optimize getting obsidian as soon as possible
        else:
            turns_with_none = max(
                math.ceil((blueprint[0]["geode"]["ore"] - (resources[0] + robots[0])) / robots[0]),
                math.ceil((blueprint[0]["geode"]["clay"] - (resources[1] + robots[1])) / robots[1]),
                math.ceil((blueprint[0]["geode"]["obsidian"] - (resources[2] + robots[2])) / robots[2]),
            )

            turns_with_ore = max(
                math.ceil((blueprint[0]["geode"]["ore"] + blueprint[0]["ore"]["ore"] - (resources[0] + robots[0])) / (robots[0] + 1)),
                math.ceil((blueprint[0]["geode"]["clay"] + blueprint[0]["ore"]["clay"] - (resources[1] + robots[1])) / robots[1]),
                math.ceil((blueprint[0]["geode"]["obsidian"] + blueprint[0]["ore"]["obsidian"] - (resources[2] + robots[2])) / robots[2]),
            )

            turns_with_clay = max(
                math.ceil((blueprint[0]["geode"]["ore"] + blueprint[0]["clay"]["ore"] - (resources[0] + robots[0])) / robots[0]),
                math.ceil((blueprint[0]["geode"]["clay"] + blueprint[0]["clay"]["clay"] - (resources[1] + robots[1])) / (robots[1] + 1)),
                math.ceil((blueprint[0]["geode"]["obsidian"] + blueprint[0]["clay"]["obsidian"] - (resources[2] + robots[2])) / robots[2]),
            )

            turns_with_obsidian = max(
                math.ceil((blueprint[0]["geode"]["ore"] + blueprint[0]["obsidian"]["ore"] - (resources[0] + robots[0])) / robots[0]),
                math.ceil((blueprint[0]["geode"]["clay"] + blueprint[0]["obsidian"]["clay"] - (resources[1] + robots[1])) / robots[1]),
                math.ceil((blueprint[0]["geode"]["obsidian"] + blueprint[0]["obsidian"]["obsidian"] - (resources[2] + robots[2])) / (robots[2] + 1)),
            )

            if can_afford(blueprint, resources, "obsidian") and turns_with_obsidian <= max(turns_with_ore, turns_with_clay, turns_with_none):
                to_build = "obsidian"
            elif can_afford(blueprint, resources, "clay") and turns_with_clay <= max(turns_with_ore, turns_with_none):
                to_build = "clay"
            elif can_afford(blueprint, resources, "ore") and turns_with_ore <= turns_with_none:
                to_build = "ore"
            else:
                to_build = None

    print(resources, robots)
    print(f"{time}: build {to_build}")

    resources = tuple(x + robots[i] for i, x in enumerate(resources))

    if to_build is not None:
        robots = tuple(x + (1 if i == ri(to_build) else 0) for i, x in enumerate(robots))
        resources = tuple(x - blueprint[0][to_build].get(rn(i), 0) for i, x in enumerate(resources))

    time -= 1
    
    return compute_blueprint(blueprint, time, robots, resources)




#print(blueprints[0])
print(evaluate_blueprint_2(blueprints[0], 24, [1, 0, 0, 0], [0, 0, 0, 0]))

#print(get_affordable(blueprints[0], [1, 0, 0, 0], [0, 0, 0, 0]))

#evaluations = [
#    max(evaluate_bluepint(blueprint, 24, (1, 0, 0, 0), (0, 0, 0, 0)))
#    for blueprint in blueprints
#]
#print(sum((i + 1) * x for i, x in enumerate(evaluations)))
