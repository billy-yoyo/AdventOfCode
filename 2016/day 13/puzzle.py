from functools import cache

OFFSET = 1358
#OFFSET = 10

@cache
def is_wall(x, y):
    value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + OFFSET
    return bin(value)[2:].count("1") % 2 == 1

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find_path_length(start, end):
    visited = set()
    state = [start]
    steps = 0
    while state:
        next_state = []
        for x, y in state:
            if x == end[0] and y == end[1]:
                return steps
            visited |= {(x, y)}
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if nx >= 0 and ny >= 0 and not is_wall(nx, ny) and (nx, ny) not in visited:
                    next_state.append((nx, ny))

        state = next_state
        steps += 1

def find_reachable(start, steps):
    visited = set()
    state = [start]
    while state and steps > 0:
        next_state = []
        for x, y in state:
            visited |= {(x, y)}
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if nx >= 0 and ny >= 0 and not is_wall(nx, ny) and (nx, ny) not in visited:
                    next_state.append((nx, ny))
        state = next_state
        steps -= 1
    return len(visited)

print(find_path_length((1, 1), (31, 39)))
print(find_reachable((1, 1), 51))