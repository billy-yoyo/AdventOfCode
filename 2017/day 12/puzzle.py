from collections import defaultdict

node_connections = defaultdict(set)

with open("input") as f:
    lines = f.read().strip().split("\n")

for line in lines:
    name, connections = line.split(" <-> ")
    node_connections[int(name.strip())] |= set([int(x) for x in connections.strip().split(", ")])

node_groups = {}

def create_group_from(start, group_index):
    node_groups[start] = group_index
    stack = [start]
    for node in stack:
        for conn in node_connections[node]:
            if conn not in node_groups:
                node_groups[conn] = group_index
                stack.append(conn)

group_start = 0
group_index = 0
while group_start is not None:
    create_group_from(group_start, group_index)
    group_index += 1
    unmarked_groups = [node for node in node_connections if node not in node_groups]
    if len(unmarked_groups) > 0:
        group_start = unmarked_groups[0]
    else:
        group_start = None

print(sum(1 for x in node_connections if node_groups[x] == 0))
print(len(set(node_groups.values())))