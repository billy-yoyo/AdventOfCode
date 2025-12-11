import math

with open("data") as f:
  positions = [[int(n) for n in x.strip().split(",")] for x in f if x.strip()]

def sqrdist(p1, p2):
  return sum((n - p2[i]) ** 2 for i, n in enumerate(p1))

pairs = [(i, j, sqrdist(positions[i], positions[j])) for i in range(len(positions)) for j in range(i)]
pairs = sorted(pairs, key=lambda x: x[2])

circuit_n = 0
circuits = {}
circuit_indices = {}

for i, j, _ in pairs:
  if i in circuits and j in circuits:
    ic, jc = circuits[i], circuits[j]
    if ic == jc:
      continue
    for k in circuit_indices[jc]:
      circuits[k] = ic
    circuit_indices[ic] |= circuit_indices[jc]
    del circuit_indices[jc]
  elif i in circuits:
    circuits[j] = circuits[i]
    circuit_indices[circuits[i]].add(j)
  elif j in circuits:
    circuits[i] = circuits[j]
    circuit_indices[circuits[j]].add(i)
  else:
    circuits[i] = circuit_n
    circuits[j] = circuit_n
    circuit_indices[circuit_n] = {i, j}
    circuit_n += 1
  
  if len(circuit_indices) == 1 and len(circuit_indices[circuits[i]]) == len(positions):
      print(positions[i][0] * positions[j][0])
      break
  
#cir_lens = sorted([len(v) for v in circuit_indices.values()])
#print(circuit_indices)
#print(math.prod(cir_lens[-3:]))