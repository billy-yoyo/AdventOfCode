from collections import defaultdict, deque
from heapq import heappop, heappush

with open("data") as f:
  device_map = {key: value.strip().split(" ") for key, value in [l.strip().split(": ") for l in f if l.strip()]}

ranks = {}
rank_stack = deque([("svr", 0)])
while len(rank_stack):
  key, rank = rank_stack.popleft()

  if key in ranks and ranks[key] == rank:
    continue

  ranks[key] = rank

  if key not in device_map:
    continue

  for conn in device_map[key]:
    rank_stack.append((conn, rank + 1))


def count_paths(start, end, count):
  counts = defaultdict(int)
  done = set()
  stack = [(ranks[start], start)]
  counts[start] = count

  while len(stack):
    _, key = heappop(stack)

    if key not in device_map:
      continue

    conns = device_map[key]
    for conn in conns:
      counts[conn] += counts[key]
      if conn not in done:
        heappush(stack, (ranks[conn], conn))
        done.add(conn)

  return counts[end]

p1 = count_paths("svr", "fft", 1)
p2 = count_paths("fft", "dac", p1)
p3 = count_paths("dac", "out", p2)
print(p3)
