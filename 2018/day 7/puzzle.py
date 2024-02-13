from collections import defaultdict

node_parents = defaultdict(list)
node_children = defaultdict(list)

nodes = set()

source = "input"

with open(source) as f:
    for line in f.read().strip().split("\n"):
        parts = line.strip().split(" ")
        parent_node, child_node = parts[1], parts[-3]
        node_children[parent_node].append(child_node)
        node_parents[child_node].append(parent_node)
        nodes |= {parent_node, child_node}

def insert_sort(x, lst, start_index):
    i = start_index
    while i < len(lst) and x > lst[i]:
        i += 1
    lst.insert(i, x)

def execute(root_nodes):
    order = []
    stack = sorted(root_nodes)
    for i, node in enumerate(stack):
        order.append(node)
        for child in node_children[node]:
            if all(pn in order for pn in node_parents[child]):
                insert_sort(child, stack, i + 1)
    return "".join(order)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def execute_parallel(root_nodes, parallelism, time_offset):
    result = []
    worker_finish_times = [0] * parallelism
    worker_current = [None] * parallelism
    stack = sorted(root_nodes)
    while stack or any(x is not None for x in worker_current):
        if any(x is not None for x in worker_current):
            next_time = min(time for i, time in enumerate(worker_finish_times) if worker_current[i] is not None)
        else:
            next_time = min(worker_finish_times)

        for i, finish_time in enumerate(worker_finish_times):
            if finish_time > next_time:
                continue
            current = worker_current[i]
            if current is not None:
                result.append(current)
                for child in node_children[current]:
                    if all(pn in result for pn in node_parents[child]):
                        insert_sort(child, stack, 0)

        for i, finish_time in enumerate(worker_finish_times):
            if finish_time > next_time:
                continue
            if len(stack) > 0:
                next_task = stack.pop(0)
                worker_current[i] = next_task
                worker_finish_times[i] = next_time + time_offset + 1 + alphabet.index(next_task)
            else:
                worker_current[i] = None
                worker_finish_times[i] = next_time

        print(f"{' ' if next_time < 10 else ''}{next_time}: {', '.join((x or '.' for x in worker_current))}")

    return max(worker_finish_times), "".join(result)

root_nodes = [node for node in nodes if len(node_parents[node]) == 0]
print(execute(root_nodes))

if source == "example":
    print(execute_parallel(root_nodes, 2, 0))
else:
    print(execute_parallel(root_nodes, 5, 60))
