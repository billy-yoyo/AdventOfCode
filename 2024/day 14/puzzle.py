from collections import defaultdict
from functools import reduce
import math

w, h, filename = 101, 103, "data"
# w, h, filename = 11, 7, "example"

with open(filename) as f:
  robots = [
    [[int(x) for x in part.split("=")[1].split(",")] for part in line.strip().split(" ")]
    for line in f.read().strip().split("\n")
  ]

robots_copy = [[[x,y],v] for (x,y),v in robots]

def move(robot):
  pos, vel = robot
  pos[0] += vel[0]
  pos[1] += vel[1]

  while pos[0] < 0:
    pos[0] += w
  while pos[0] >= w:
    pos[0] -= w

  while pos[1] < 0:
    pos[1] += h
  while pos[1] >= h:
    pos[1] -= h

for _ in range(100):
  for robot in robots:
    move(robot)

w2 = w // 2
h2 = h // 2

def get_quad(pos):
  x, y = pos
  qx, qy = None, None
  if x < w2:
    qx = 0
  elif x > w2:
    qx = 1

  if y < h2:
    qy = 0
  elif y > h2:
    qy = 1
  
  if qx is not None and qy is not None:
    return (qx, qy)
  return None

quad_counts = defaultdict(int)
for rpos, _ in robots:
  quad = get_quad(rpos)
  if quad is not None:
    quad_counts[quad] += 1

def print_robos(robots):
  return ("\n".join("".join(str(len([1 for (rx,ry),_ in robots if rx==x and ry==y])) if any(rx == x and ry == y for (rx, ry), _ in robots) else "." for x in range(w)) for y in range(h)))

safety = reduce(lambda x,y: x*y, quad_counts.values(), 1)
print(safety)

def has_robot(robots, x, y):
  return any(rx == x and ry == y for (rx,ry), _ in robots)

def robo_cycle_length(robot):
  _, (vx, vy) = robot
  # vx * t = w * d
  # t = (w*d)/vx
  # vy * t = h * d
  # (w*d)*vy/vx = h*d
  # d(w*vy/vx - h) = 0
  # w*vy/vx = h
  # w*vy = h*vx
  # 
  xlcm = abs(math.lcm(vx, w) // w)
  ylcm = abs(math.lcm(vy, h) // h)
  return math.lcm(xlcm, ylcm)

cycle = 1
for robot in robots:
  cycle = math.lcm(robo_cycle_length(robot), cycle)

def find_tree():
  robots = robots_copy
  for i in range(6475):
    for robot in robots:
      move(robot)

    rmap = set()
    for (x,y),_ in robots:
      rmap.add((x,y))

    longest_line = 0
    for x,y in rmap:
      line = 0
      while (x,y) in rmap:
        y += 1
        line += 1
      longest_line = max(line, longest_line)

    #if longest_line > 5:
  print(print_robos(robots))
  print(i)
      

find_tree()

# 103724
# 114127

# first cycle: 10097
# cycle length: 10403

# ~110
# 314
# 718


