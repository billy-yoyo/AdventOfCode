from collections import defaultdict, deque

w, h, filename, max_drop = 70, 70, "data", 1024
#w, h, filename, max_drop = 6, 6, "example", 12

grid = defaultdict(int)

with open(filename) as f:
  for i, pair in enumerate(f.read().strip().split("\n")):
    x, y = [int(x) for x in pair.strip().split(",")]
    grid[(x, y)] = i + 1

offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]
def find_path(end, max_drop):
  ex, ey = end
  visited = set()
  stack = deque([(0, 0, [])])
  steps = 0
  while stack:
    next_stack = deque([])
    for x, y, path in stack:
      if (x, y) in visited:
        continue

      visited.add((x, y))

      if x == ex and y == ey:
        return path + [(x, y)]

      for ox, oy in offsets:
        nx, ny = x + ox, y + oy
        if nx < 0 or nx > w or ny < 0 or ny > h:
          continue

        dest_time = grid[(nx, ny)]
        if (dest_time == 0 or dest_time > max_drop):
          next_stack.append((nx, ny, path + [(x, y)]))
    stack = next_stack
    steps += 1

def find_lowest_byte(start_max_drop):
  end = (w, h)
  max_drop = start_max_drop
  path = find_path(end, max_drop)
  while path is not None:
    max_drop = min(grid[pos] for pos in path if grid[pos] > max_drop)
    path = find_path(end, max_drop)
  
  return next(pos for pos, drop in grid.items() if drop == max_drop)


print(len(find_path((w, h), max_drop)))
print(find_lowest_byte(max_drop))
