
with open("data") as f:
  data = f.read().strip().split("\n\n")

def parse_game(data):
  lines = data.strip().split("\n")
  a = [int(x.strip()[1:]) for x in lines[0].split(":")[1].strip().split(",")]
  b = [int(x.strip()[1:]) for x in lines[1].split(":")[1].strip().split(",")]
  prize = [int(x.strip()[2:]) for x in lines[2].split(":")[1].strip().split(",")]
  return (a, b, prize)

def is_int(x):
  return abs(x - round(x)) < 0.001

def game_cost(game, add=0):
  a, b, prize = game
  prize = [x + add for x in prize]
  # (d * ax) + (t * bx) = x
  # d = (x - (t*bx)) / ax
  # (d * ay) + (t * by) = y
  # ((x - (t*bx)) * ay / ax) + (t * by) = y
  # (x - (t*bx)) * ay/ax = y - (t*by)
  # (x*ay/ax) + (t*by) - (t*bx*ay/ax) = y
  # t*(by - bx*ay/ax) = y - (x*ay/ax)

  grad = a[1]/a[0]
  numer = prize[1] - (prize[0]*grad)
  denom = b[1] - (b[0]*grad)

  if denom == 0:
    return None
  
  # b steps
  t = numer / denom
  # a steps
  d = (prize[0] - (t * b[0])) / a[0]

  if not is_int(t) or not is_int(d):
    return None
  
  t, d = round(t), round(d)

  #print(t, d)
  return (d*3) + t

games = [parse_game(game) for game in data]

total_cost = 0
for game in games:
  cost = game_cost(game, add=10000000000000)
  if cost:
    total_cost += cost

print(total_cost)
