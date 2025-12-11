from collections import defaultdict
from itertools import combinations

graph = defaultdict(set)
conns = set()

triplets = []

with open("data") as f:
  for line in f.read().strip().split("\n"):
    a, b = line.strip().split("-")
    conns.add(tuple(sorted([a, b])))
    graph[a].add(b)
    graph[b].add(a)
  
for a, b in conns:
  for c in graph[a] & graph[b]:
    triplet = {a,b,c}
    if triplet not in triplets:
      triplets.append(triplet)

def collapse_once_old(subgraphs):
  membership = defaultdict(set)
  for i, sg in enumerate(subgraphs):
    for x in sg:
      membership[x].add(i)
  
  found = set()
  new_subgraphs = []
  for x, sgis in membership.items():
    if x in found:
      continue
    if len(sgis) == len(subgraphs[0]):
      vals = set()
      for sgi in sgis:
        for val in subgraphs[sgi]:
          vals.add(val)
      
      if len(vals) == len(subgraphs[0]) + 1:
        new_subgraphs.append(vals)
        for val in vals:
          found.add(val)
  
  return new_subgraphs

def collapse_once(subgraphs):
  membership = defaultdict(set)
  for i, sg in enumerate(subgraphs):
    for x in sg:
      membership[x].add(i)

  done = set()
  new_subgraphs = []
  for i, sg1 in enumerate(subgraphs):
    js = set()
    for x in sg1:
      js |= membership[x]
    
    for j in js:
      if i == j:
        continue
      key = (min(i,j), max(i,j))
      if key in done:
        continue
      done.add(key)
      sg2 = subgraphs[j]

      if len(sg1 & sg2) == len(sg1) - 1:
        node1 = next(iter(sg1 - sg2))
        node2 = next(iter(sg2 - sg1))
        
        if node2 in graph[node1]:
          nsg = sg1 | sg2
          if nsg not in new_subgraphs:
            new_subgraphs.append(nsg)
  return new_subgraphs


def collapse_once_new(subgraphs):
  membership = defaultdict(set)
  for i, sg in enumerate(subgraphs):
    for x in sg:
      membership[x].add(i)

  good_subgraphs = set()
  for i, sg in enumerate(subgraphs):
    if all(len(membership[x]) >= len(sg) for x in sg):
      good_subgraphs.add(i) 

  new_subgraphs = []
  for i in good_subgraphs:
    sg1 = subgraphs[i]
    for j in range(i):
      if j not in good_subgraphs:
        continue
      sg2 = subgraphs[j]

      if len(sg1 & sg2) == len(sg1) - 1:
        nsg = set(sg1 | sg2)
        if nsg not in new_subgraphs and len(nsg) == sum(1 for sg in subgraphs if sg < nsg):
          new_subgraphs.append(nsg)
  return list(new_subgraphs)


def collapse(subgraphs):
  while True:
    next_subgraphs = collapse_once(subgraphs)
    print(next_subgraphs)
    print(f"{len(subgraphs)} -> {len(next_subgraphs)}")
    if not next_subgraphs:
      return subgraphs
    subgraphs = next_subgraphs


print(sum(1 for t in triplets if any(x[0] == "t" for x in t)))

parties = collapse(triplets)
print(parties)

party = parties[0]
print(",".join(sorted(party)))
