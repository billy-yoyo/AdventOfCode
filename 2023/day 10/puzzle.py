from collections import defaultdict

NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3
dir_map = {
  "|": (NORTH, SOUTH),
  "-": (EAST, WEST),
  "L": (NORTH, EAST),
  "J": (NORTH, WEST),
  "7": (SOUTH, WEST),
  "F": (SOUTH, EAST),
}

offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]

opposite = [SOUTH, WEST, EAST, NORTH]

with open("input") as f:
  tiles = f.read().strip().split("\n")
  start = [(x, y) for y, l in enumerate(tiles) for x, c in enumerate(l) if c == "S"][0]

def get(pos, dx=0, dy=0):
  x, y = pos[0] + dx, pos[1] + dy
  if y < 0 or y >= len(tiles):
    return "."
  elif x < 0 or x >= len(tiles[y]):
    return "."
  else:
    return tiles[y][x]

pos = []

if get(start, 1, 0) in "-J7":
  pos = (start[0] + 1, start[1])
elif get(start, 0, 1) in "|LJ":
  pos = (start[0], start[1] + 1)
elif get(start, -1, 0) in "-LF":
  pos = (start[0] - 1, start[1])
else:
  pos = (start[0], start[1] - 1)

visited = [start]
hits = defaultdict(bool)
hits[start] = True
hits[pos] = True
loop_sides = defaultdict(lambda: 0)

last_offset = None
outside = None

while pos[0] != start[0] or pos[1] != start[1]:
  char = get(pos)
  directions = dir_map[char]
  doff = [offsets[d] for d in directions]
  for offset in doff:
    npos = (pos[0] + offset[0], pos[1] + offset[1])
    if npos[0] != visited[-1][0] or npos[1] != visited[-1][1]:
      if last_offset is None:
        last_offset = offset
        if offset[0] == 1:
          outside = NORTH
        elif offset[0] == -1:
          outside = SOUTH
        elif offset[1] == 1:
          outside = WEST
        else:
          outside = EAST

      visited.append(pos)
      hits[npos] = True

      if last_offset[0] != offset[0] or last_offset[1] != offset[1]:
        outside_off = offsets[outside]
        inside_off = offsets[opposite[outside]]

        loop_sides[(pos[0] + outside_off[0], pos[1] + outside_off[1])] = 1
        loop_sides[(pos[0] + inside_off[0], pos[1] + inside_off[1])] = -1

        # check which side is outside now
        if offset[1] == 1:
          if outside == NORTH and last_offset[0] == 1:
            outside = EAST
          elif outside == NORTH and last_offset[0] == -1:
            outside = WEST
          elif outside == SOUTH and last_offset[0] == 1:
            outside = WEST
          else:
            outside = EAST
        elif offset[1] == -1:
          if outside == NORTH and last_offset[0] == 1:
            outside = WEST
          elif outside == NORTH and last_offset[0] == -1:
            outside = EAST
          elif outside == SOUTH and last_offset[0] == 1:
            outside = EAST
          else:
            outside = WEST
        elif offset[0] == 1:
          if outside == WEST and last_offset[1] == -1:
            outside = NORTH
          elif outside == WEST and last_offset[1] == 1:
            outside = SOUTH
          elif outside == EAST and last_offset[0] == -1:
            outside = SOUTH
          else:
            outside = NORTH
        else:
          if outside == WEST and last_offset[1] == -1:
            outside = SOUTH
          elif outside == WEST and last_offset[1] == 1:
            outside = NORTH
          elif outside == EAST and last_offset[0] == -1:
            outside = NORTH
          else:
            outside = SOUTH
        
        last_offset = offset

      outside_off = offsets[outside]
      inside_off = offsets[opposite[outside]]

      loop_sides[(pos[0] + outside_off[0], pos[1] + outside_off[1])] = 1
      loop_sides[(pos[0] + inside_off[0], pos[1] + inside_off[1])] = -1

      pos = npos
      break


def get_char(x, y):
  side = loop_sides[(x, y)]
  if hits[(x, y)]:
    return tiles[y][x]
  elif side == 1:
    return "x"
  elif side == -1:
    return "y"
  else:
    return "."

new_tiles = "\n".join([
  "".join([get_char(x, y) for x, c in enumerate(l)]) for y, l in enumerate(tiles)
])

print(new_tiles)



def find_side():
  start = (-1, -1)

  stack = [start]
  while len(stack) > 0:
    new_stack = []
    for pos in stack:
      if loop_sides[(pos[0], pos[1])] != 0:
        return pos
      hits[pos] = True
      for offset in offsets:
        npos = (pos[0] + offset[0], pos[1] + offset[1])
        if npos[0] >= -1 and npos[1] >= -1 and npos[0] <= len(tiles[0]) and npos[1] <= len(tiles) and not hits[npos]:
          hits[npos] = True
          new_stack.append(npos)
    stack = new_stack
  return None

print(f"finding side...")
pos = find_side()

outside_side = loop_sides[(pos[0], pos[1])]
inside_side = -1 if outside_side == 1 else 1
print(f"outside side is {outside_side}")

visited_inside = defaultdict(bool)
stack = [pos for pos, side in loop_sides.items() if side == inside_side and not hits[pos]]
print(f"initial inside stack is {len(stack)}")
for pos in stack:
  visited_inside[pos] = True

while len(stack) > 0:
  new_stack = []
  for pos in stack:
    for offset in offsets:
      npos = (pos[0] + offset[0], pos[1] + offset[1])
      if npos[0] >= 0 and npos[1] >= 0 and npos[0] < len(tiles[0]) and npos[1] < len(tiles) and not hits[npos] and not visited_inside[npos]:
        visited_inside[npos] = True
        new_stack.append(npos)
  stack = new_stack
  print(f"next stack is {len(stack)}")

outside_area = sum(hits.values())
total_area = len(tiles[0]) * len(tiles)
inside_area = total_area - outside_area

print(len(visited) // 2)
print(sum(visited_inside.values()))


