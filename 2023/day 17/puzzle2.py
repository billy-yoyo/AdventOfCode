
with open("input") as f:
    lines = f.read().strip().split("\n")

heat_map = [[int(x) for x in line] for line in lines]

width = len(lines[0])
height = len(lines)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def take_best(lst, key):
    best = None
    for i, x in enumerate(lst):
        value = key(x)
        if best is None or value < best[1]:
            best = (i, value, x)

    del lst[best[0]]
    return best[2]

def oob(x, y):
    return x < 0 or x >= width or y < 0 or y >= height

# find lowest simple path
def find_simple():
  lowest = {}
  stack = [(0, 0, 0)]
  for x in stack:
      lowest[x] = 0

  while stack:
      x, y, dir, steps = take_best(stack, lambda x: lowest[x])

      for new_dir in range(4):
          if (new_dir + 2) % 4 == dir:
            continue

          if new_dir == dir and steps >= 3:
            continue

          new_steps = steps + 1 if new_dir == dir else 1
          ox, oy = offsets[new_dir]
          nx, ny = x + ox, y + oy
          if oob(nx, ny):
              continue

          key = (nx, ny, new_dir, new_steps)

          heat = lowest[(x, y, dir, steps)]
          cur_heat = heat_map[ny][nx] + heat
          
          if nx == width - 1 and ny == height - 1:
              return cur_heat

          if key in lowest and lowest[key] < cur_heat:
              continue
          
          lowest[key] = cur_heat

          if key not in stack:
              stack += [key]
  return -1

def find_ultra():
    lowest = {}
    stack = [(0, 0, EAST, 0), (0, 0, SOUTH, 0)]
    for x in stack:
        lowest[x] = 0

    while stack:
        x, y, dir, steps = take_best(stack, lambda x: lowest[x])
        heat = lowest[(x, y, dir, steps)]

        if x == width - 1 and y == height - 1:
            return heat

        for new_dir in range(4):
            if (new_dir + 2) % 4 == dir:
                continue
            
            ox, oy = offsets[new_dir]
            cur_heat = heat
            if new_dir == dir:
                if steps >= 10:
                    continue
                
                new_steps = steps + 1
                nx, ny = x + ox, y + oy
                if oob(nx, ny):
                    continue
                cur_heat += heat_map[ny][nx]
            else:
                new_steps = 4
                cur_heat = heat
                nx, ny = x, y
                for _ in range(4):
                    nx, ny = nx + ox, ny + oy
                    if not oob(nx, ny):
                        cur_heat += heat_map[ny][nx]
                if oob(nx, ny):
                    continue
            

            key = (nx, ny, new_dir, new_steps)
            #if nx == width - 1 and ny == height - 1:
            #    return cur_heat

            if key in lowest and lowest[key] < cur_heat:
                continue
            
            lowest[key] = cur_heat

            if key not in stack:
                stack += [key]
    return -1

print(find_ultra())

