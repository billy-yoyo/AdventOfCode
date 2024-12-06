
with open("data") as f:
  rows = [line.strip() for line in f.read().strip().split("\n")]

width, height = len(rows[0]), len(rows)
sx, sy = next((x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c in "<>v^")

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

direction_map = {
  ">": (1, 0),
  "<": (-1, 0),
  "^": (0, -1),
  "v": (0, 1)
}



def get_path_length(block_patch=None):
  x, y = sx, sy

  visited = set()
  visited_with_dir = set()
  dindex = directions.index(direction_map[rows[y][x]])

  def get(x, y):
    if block_patch is not None and (x, y) == block_patch:
      return "#"
    else:
      return rows[y][x]

  step = 0
  while True:
    visited.add((x, y))

    if (x, y, dindex) in visited_with_dir:
      return None

    visited_with_dir.add((x, y, dindex))

    dx, dy = directions[dindex]
    x, y = x + dx, y + dy
    step += 1
    if x < 0 or y < 0 or x >= width or y >= height:
      break
    elif get(x, y) == "#":
      x, y = x - dx, y - dy
      dindex = (dindex + 1) % len(directions)
  
  return visited

path = get_path_length()
print(len(path))

loop_positions = 0
for block in path:
  if block != (sx, sy) and get_path_length(block) is None:
    loop_positions += 1
  
print(loop_positions)
