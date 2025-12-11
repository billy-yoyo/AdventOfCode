from collections import defaultdict

with open("input") as f:
    input = f.read()

graph = defaultdict(list)

def add_connection(start, end):
    graph[start].append(end)
    graph[end].append(start)

for line in input.strip().split("\n"):
    start, end = line.strip().split("-")
    add_connection(start, end)


def find_paths(start, end, cur_path=None, revisited=False):
    if cur_path is None:
        cur_path = []
    
    cur_path = cur_path + [start]
    
    for connection in graph[start]:
        if connection == end:
            yield cur_path + [end]
        elif connection.upper() == connection or connection not in cur_path:
            yield from find_paths(connection, end, cur_path, revisited)
        elif not revisited and connection != "start":
            yield from find_paths(connection, end, cur_path, True)

n = 0
for path in find_paths("start", "end"):
    n += 1
print(n)