import math

fields = ["capacity", "durability", "flavor", "texture", "calories"]
items = {}
item_names = []

def read_item(line):
    name, fields = line.split(":")
    name = name.strip()
    fields = [field.strip().split(" ") for field in fields.strip().split(",")]
    fields = {name: int(value) for name, value in fields}

    items[name] = fields
    item_names.append(name)

with open("data") as f:
    for line in f:
        read_item(line.strip())

def evaluate_field(field, dist):
    return sum(dist[item] * items[item][field] for item in items)

def evaluate_dist(dist):
    total = 1
    for field in fields:
        if field == "calories":
            continue
        
        total *= max(0, evaluate_field(field, dist))
    return total

def iterate_dists(remaining=100, item_index=0, dist=None):
    if dist is None:
        dist = {item: 0 for item in items}

    if item_index >= len(item_names):
        # ensure dist produces exactly 500 calories
        if evaluate_field("calories", dist) == 500:
            yield dist
    else:
        for i in range(remaining + 1):
            dist[item_names[item_index]] = i
            yield from iterate_dists(remaining=remaining-i, item_index=item_index+1, dist=dist)

def optimize_dist():
    return max(evaluate_dist(dist) for dist in iterate_dists())

print(optimize_dist())