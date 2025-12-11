
with open("input") as f:
    data = [[int(x) for x in line.strip().split("/")] for line in f.read().strip().split("\n")]

stack = [[(i, 1)] for i, x in enumerate(data) if x[0] == 0] + [[(i, 0)] for i, x in enumerate(data) if x[1] == 0] 

best_length_bridges = []
best_length = 0
for path in stack:
    path_strength = sum(sum(data[x]) for x, _ in path)

    matches = 0
    last_id = data[path[-1][0]][path[-1][1]]
    for i, item in enumerate(data):
        if item[0] == last_id and all(i != x for x, _ in path):
            matches += 1
            stack.append(path + [(i, 1)])
        elif item[1] == last_id and all(i != x for x, _ in path):
            matches += 1
            stack.append(path + [(i, 0)])
    
    if len(path) > best_length:
        best_length = len(path)
        best_length_bridges = [path_strength]
    elif len(path) == best_length:
        best_length_bridges.append(path_strength)

print(max(best_length_bridges)) 

