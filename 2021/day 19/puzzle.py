
with open("input") as f:
    input = f.read()

scanner_lines = input.strip().split("\n\n")

scanners = []
for lines in scanner_lines:
    scanner = []
    for line in lines.split("\n"):
        if line.strip() and not line.strip().startswith("---"):
            scanner.append(tuple([int(x) for x in line.strip().split(",")]))
    scanners.append(scanner)

def overlap(s1_positions, s2_rotations):
    for rotation in s2_rotations:
        for point in rotation:
            for init_point in s1_positions:
                diff = [v1 - v2 for v1, v2 in zip(init_point, point)]
                count = sum([tuple(v + d for v, d in zip(p, diff)) in s1_positions for p in rotation])
                if count >= 12:
                    print(diff)
                    return [tuple(v + d for v, d in zip(p, diff)) for p in rotation]
    return None

def roll(v): return (v[0],v[2],-v[1])
def turn(v): return (-v[1],v[0],v[2])
def sequence (v):
    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield(v)           #    Yield R
            for i in range(3): #    Yield TTT
                v = turn(v)
                yield(v)
        v = roll(turn(roll(v)))  # Do RTR

def get_rotations(scanner):
    return sorted(zip(*[sequence(v) for v in scanner]))

rotations = [get_rotations(scanner) for scanner in scanners]
#beacons = set(scanners[0])
#normalized_scanners = [(0, scanners[0])]

#for i, rotation in enumerate(rotations[0]):
#    if overlap(rotation, rotations[1]) is None:
#        print(f"no overlap for rotation {i}??")
#print("--")

#normalized = overlap(scanners[0], rotations[1])
#print("--")
#overlap(normalized, rotations[4])
"""
lookup4 = [
    (459,-707,401),
    (-739,-1745,668),
    (-485,-357,347),
    (432,-2009,850),
    (528,-643,409),
    (423,-701,434),
    (-345,-311,381),
    (408,-1815,803),
    (534,-1912,768),
    (-687,-1600,576),
    (-447,-329,318),
    (-635,-1737,486)
]

lookup1 = [
    (459,-707,401),
    (-739,-1745,668),
    (-485,-357,347),
    (432,-2009,850),
    (528,-643,409),
    (423,-701,434),
    (-345,-311,381),
    (408,-1815,803),
    (534,-1912,768),
    (-687,-1600,576),
    (-447,-329,318),
    (-635,-1737,486)
]

diff4 = [-20,-1133,1061]
diff1 = [68,-1246,-43]

lookup, diff = lookup4, diff4

aligned = rotations[4][5]

# p + d IN N
# Exists some n IN N s.t. D = p - n

for rotation in rotations[4]:
    count = sum(tuple([v + d for v, d in zip(p, diff)]) in normalized for p in rotation)
    print(count)
"""

beacons = set(scanners[0])
todo = [scanners[0]]
rotations.pop(0)

while todo:
    scanner = todo.pop(0)
    new_rotations = []
    for i, rot in enumerate(rotations):
        normalized = overlap(scanner, rot)
        if normalized:
            todo.append(normalized)
            beacons |= set(normalized)
        else:
            new_rotations.append(rot)
    rotations = new_rotations

print(len(beacons))
