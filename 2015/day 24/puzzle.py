import itertools 

with open("weights", "r") as f:
    weights = [int(line.strip()) for line in f.readlines()]

total_weight = sum(weights)
group_weight = total_weight // 4

print(group_weight)

class Node:
    def __init__(self, value, child):
        self.value = value
        self.total = value + (child.value if child else 0)
        self.child = child

    def __str__(self):
        if self.child:
            return f"{self.value} + {self.child}"
        else:
            return str(self.value)

def groups_of_size(weights, size):
    for subset in itertools.combinations(weights, size):
        if sum(subset) == group_weight:
            yield subset

def has_group_of_size(weights, size):
    for subset in groups_of_size(weights, size):
        return True
    return False

def has_group_of_size_and_other_group(weights, size):
    for subset in groups_of_size(weights, size):
        remaining_weights = [w for w in weights if w not in subset]
        for i in range(4, len(remaining_weights) - 4):
            if has_group_of_size(remaining_weights, i):
                return True
    return False
    

def prod(s):
    n = 1
    for x in s:
        n *= x
    return n

subsets = sorted([(s, prod(s)) for s in groups_of_size(weights, 4)], key=lambda p: p[1])

def get_best_quant():
    for subset, quant in subsets:
        remaining_weights = [w for w in weights if w not in subset]
        for i in range(4, len(remaining_weights) - 4):
            if has_group_of_size_and_other_group(remaining_weights, i):
                return quant
    return None

print(get_best_quant())

"""
def groupings(index=0):
    if index >= len(weights):
        yield None
        return
    else:
        weight = weights[index]
        for subgroup in groupings(index=index + 1):
            if subgroup and subgroup.total > group_weight:
                continue
            yield subgroup
            yield Node(weight, subgroup)

ordered_groupings = sorted([g for g in groupings(0) if g and g.total == group_weight])

for og in ordered_groupings:
    print(og)"""