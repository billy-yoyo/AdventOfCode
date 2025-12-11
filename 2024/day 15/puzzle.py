
with open("data") as f:
  mapdata, movedata = f.read().strip().split("\n\n")

mapdata = [x.strip()[1:-1] for x in mapdata.strip().split("\n")[1:-1]]

walls = set((x*2, y) for y, line in enumerate(mapdata) for x, c in enumerate(line) if c == "#")
boxes = set((x*2, y) for y, line in enumerate(mapdata) for x, c in enumerate(line) if c == "O")
pos = next((x*2, y) for y, line in enumerate(mapdata) for x, c in enumerate(line) if c == "@")

dir_map = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
moves = [c for c in movedata.strip().replace("\n", "")]

w = len(mapdata[0]) * 2
h = len(mapdata)

def in_bounds(x, y):
  return 0 <= x < w and 0 <= y < h

def has_box(x, y):
  return (x, y) in boxes or (x - 1, y) in boxes

def has_wall(x, y):
  return (x, y) in walls or (x - 1, y) in walls

def find_box(x, y):
  if (x, y) in boxes:
    return (x, y)
  return (x - 1, y)

def step(pos, dir):
  px, py = pos
  dx, dy = dir

  old_boxes = set()
  last_layer = ((px, py),)
  while len(last_layer) > 0:
    next_layer = set()
    for x, y in last_layer:
      nx, ny = x + dx, y + dy
      if has_wall(nx, ny) or not in_bounds(nx, ny):
        return pos
      elif has_box(nx, ny):
        bx, by = find_box(nx, ny)
        old_boxes.add((bx, by))
        if dy != 0:
          next_layer.add((bx, by))
          next_layer.add((bx+1, by))
        elif dx > 0:
          next_layer.add((bx+1, by))
        else:
          next_layer.add((bx, by))
    last_layer = next_layer
  
  mx, my = px + dx, py + dy
  if len(old_boxes) > 0:
    new_boxes = set()
    for bx, by in old_boxes:
      new_boxes.add((bx + dx, by + dy))

    for box in (old_boxes - new_boxes):
      boxes.remove(box)
    for box in (new_boxes - old_boxes):
      boxes.add(box)
    
  return (mx, my)

def print_map():
  print("\n".join("".join("#" if has_wall(x, y) else ("O" if has_box(x, y) else ("@" if (x, y) == pos else ".")) for x in range(w)) for y in range(h)))

for move in moves:
  #print_map()
  #print(f"-- {move}")
  pos = step(pos, dir_map[move])


#print_map()

print(sum(x + 2 + (100*(y + 1)) for x, y in boxes))



