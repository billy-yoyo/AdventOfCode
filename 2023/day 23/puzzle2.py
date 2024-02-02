

with open("input") as f:
    lines = f.read().strip().split("\n")

height = len(lines)
width = len(lines[0])

start = tuple([(x, 0) for x, c in enumerate(lines[0]) if c == "."][0])
end = tuple([(x, height - 1) for x, c in enumerate(lines[-1]) if c == "."][0])

def get_c(x, y):
    if 0 <= y < height and 0 <= x < width:
        c = lines[y][x]
        return "." if c in "<>v^" else c
    
    return "#"

offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]


crossroads = [start]
for x in range(width):
    for y in range(height):
        c = get_c(x, y)
        if c == ".":
            adj = sum(1 for ox, oy in offsets if get_c(x + ox, y + oy) == ".")
            if adj > 2:
                crossroads.append((x, y))

crossroads.append(end)


def find_connections(start):
    connected = []
    sx, sy = start
    stack = [((sx + ox, sy + oy), 1) for ox, oy in offsets if get_c(sx + ox, sy + oy) == "."]
    visited = {(sx, sy)}
    for (x, y), length in stack:
        visited |= {(x, y)}
        for ox, oy in offsets:
            nx, ny = x + ox, y + oy
            if (nx, ny) in visited or get_c(nx, ny) != ".":
                continue
            
            if (nx, ny) in crossroads:
                connected.append((crossroads.index((nx, ny)), length))
                visited |= {(nx, ny)}
            else:
                stack.append(((nx, ny), length + 1))
    return connected

connections = [find_connections(start) for start in crossroads]

print(f"calculated connections")

end_paths = []

stack = [([0], 1)]
for path, length in stack:
    for conn, conn_length in connections[path[-1]]:
        if conn == len(connections) - 1:
            end_paths.append((length + conn_length, path))
            print(length + conn_length)
        if conn not in path:
            stack.append((path + [conn], length + conn_length + 1))



#print("\n".join([
#    "".join(str(crossroads.index((x, y))) if (x, y) in crossroads else c for x, c in enumerate(line)) for y, line in enumerate(lines)
#]))

print(max(end_paths))
