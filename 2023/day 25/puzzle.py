from collections import defaultdict

connections = defaultdict(list)

with open("input") as f:
    for line in f.read().strip().split("\n"):
        left, right = line.strip().split(": ")
        for target in right.strip().split(" "):
            connections[left].append(target)
            connections[target].append(left)

nodes = list(connections.keys())
def find_shortest_path(a, b):
    stack = [[a]]
    while stack:
        next_stack = []
        for path in stack:
            for conn in connections[path[-1]]:
                if conn == b:
                    return path + [b]
                elif conn not in path:
                    next_stack.append(path + [conn])
        stack = next_stack
    return []

def find_shortest_path_without_edge(a, b):
    stack = [[a]]
    while stack:
        next_stack = []
        for path in stack:
            for conn in connections[path[-1]]:
                if (path[-1] == a or path[-1] == b) and (conn == a or conn == b):
                    continue

                if conn == b:
                    return path + [b]
                elif conn not in path:
                    next_stack.append(path + [conn])
        stack = next_stack
    return []

def find_critical_edges():
    edge_shortest_paths = {}
    for a in connections:
        for b in connections[a]:
            key = f"{a}-{b}" if a < b else f"{b}-{a}"
            if key not in edge_shortest_paths:
                edge_shortest_paths[key] = len(find_shortest_path_without_edge(a, b))
    return edge_shortest_paths


snipped_edges = sorted(find_critical_edges().items(), key=lambda x: x[1])[-3:]

print(snipped_edges)
for snipped, _ in snipped_edges:
    left, right = snipped.split("-")
    connections[left].remove(right)
    connections[right].remove(left)

groups = defaultdict(int)
group_index = 1

for node in connections:
    if groups[node] > 0:
        continue

    stack = [node]
    for item in stack:
        groups[item] = group_index
        for conn in connections[item]:
            if groups[conn] == 0:
                stack.append(conn)

    group_index += 1

prod = 1
for i in range(1, group_index):
    size = sum(1 for v in groups.values() if v == i)
    prod *= size 
    print(f"group {i} has {size} items")

print(prod)
