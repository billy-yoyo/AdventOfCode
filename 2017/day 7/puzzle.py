from collections import defaultdict
from functools import cache

with open("input") as f:
    data = f.read().strip().split("\n")

node_weights = {}
node_children = defaultdict(list)
node_parents = defaultdict(list)

for line in data:
    parts = line.split("->")
    name, weight = parts[0].strip().split(" ")
    weight = int(weight[1:-1])
    node_weights[name] = weight

    if len(parts) > 1:
        child_names = parts[1].strip().split(", ")
        node_children[name] = child_names
        for child in child_names:
            node_parents[child].append(name)

root_node = next(node for node in node_weights if len(node_parents[node]) == 0)

@cache
def total_node_weight(root_node):
    total_weight = node_weights[root_node]
    for child in node_children[root_node]:
        total_weight += total_node_weight(child)
    return total_weight

def find_bad_node_weight(root_node):
    if len(node_children[root_node]) == 0:
        sibling_weights = [total_node_weight(child) for child in node_children[node_parents[root_node][0]] if child != root_node]
        return sibling_weights[0]
    
    children_weights = {child: total_node_weight(child) for child in node_children[root_node]}
    weight_counts = defaultdict(int)
    for _, weight in children_weights.items():
        weight_counts[weight] += 1

    if any(count == 1 for count in weight_counts.values()):
        wrong_weight = next(weight for weight, count in weight_counts.items() if count == 1)
        wrong_child = next(child for child, weight in children_weights.items() if weight == wrong_weight)
        return find_bad_node_weight(wrong_child)
    else:
        # this nodes weight is wrong!
        total_child_weights = sum(w for w in children_weights.values())
        sibling_weights = [total_node_weight(child) for child in node_children[node_parents[root_node][0]] if child != root_node]
        return sibling_weights[0] - total_child_weights


print(find_bad_node_weight(root_node))
