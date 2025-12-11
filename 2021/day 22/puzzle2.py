
def overlap(p1, p2):
    return p1[0] <= p2[1] and p2[0] <= p1[1]

def inside(p1, p2):
    return p2[0] <= p1[0] and p1[1] <= p2[1]

class RangeMap:
    def __init__(self, ranges=None):
        self.ranges = ranges if ranges is not None else []

    def copy(self):
        ranges = [[list(r), val.copy() if isinstance(val, RangeMap) else val] for r, val in self.ranges]
        return RangeMap(ranges)

    def add_value(self, rval, value):
        if isinstance(rval, RangeMap):
            return rval.copy().add_range(value[0], value[1:])
        else:
            return value[0]

    def create_value(self, value):
        if len(value) == 1:
            return value[0]
        else:
            return RangeMap().add_range(value[0], value[1:])

    def copy_value(self, rval):
        if isinstance(rval, RangeMap):
            return rval.copy()
        else:
            return rval

    def add_range(self, r, value):
        if len(value) == 0:
            return self
        original_r = list(r)
        original_ranges = self.copy()
        r = list(r)
        new_ranges = []
        for pair in self.ranges:
            range, rval = pair
            if overlap(r, range):
                # r is inside range
                if inside(r, range):
                    #print(f"* new {r} is inside old {range} ({value})")
                    if r[0] == range[0] and r[1] == range[1]:
                        pair[1] = self.add_value(rval, value)
                    else:
                        #print(f"  - creating new range at {r} ({value})")
                        new_ranges.append([r, self.add_value(rval, value)])
                        if r[0] == range[0]:
                            #print(f"  - moved old left to {r[1] + 1} ({value})")
                            range[0] = r[1] + 1
                        elif r[1] == range[1]:
                            #print(f"  - moved old right to {r[0] - 1} ({value})")
                            range[1] = r[0] - 1
                        else:
                            #print(f"  - creating new range at {[r[1] + 1, range[1]]} ({value})")
                            new_ranges.append([[r[1] + 1, range[1]], self.copy_value(rval)])
                            range[1] = r[0] - 1
                    r = None
                    break
                elif inside(range, r):
                    #print(f"* old {range} is inside new {r} ({value})")
                    if r[0] != range[0]:
                        self.add_range([r[0], range[0] - 1], value)
                    if r[1] != range[1]:
                        self.add_range([range[1] + 1, r[1]], value)

                    if isinstance(rval, RangeMap):
                        rval.add_range(value[0], value[1:])
                    else:
                        pair[1] = value[0]
                    
                    return self
                elif r[0] < range[0]:
                    #print(f"* {r} overlaps {range} to the left ({value})")
                    new_ranges.append([[range[0], r[1]], self.add_value(rval, value)])
                    rl = range[0]
                    range[0] = r[1] + 1
                    r[1] = rl - 1
                else:
                    #print(f"* {r} overlaps {range} to the right ({value})")
                    new_ranges.append([[r[0], range[1]], self.add_value(rval, value)])
                    ru = range[1]
                    range[1] = r[0] - 1
                    r[0] = ru + 1
        if r is not None:
            new_ranges.append([r, self.create_value(value)])
        if any(p[0] > p[1] for p, _ in new_ranges):
            raise Exception(f"Adding {original_r} caused a range to flip")
        self.ranges += new_ranges
        if any(any(i != j and overlap(p1[0], p2[0]) for i, p2 in enumerate(self.ranges)) for j, p1 in enumerate(self.ranges)):
            raise Exception(f"Adding {original_r} caused an overlap to appear in the new ranges {new_ranges}")
        return self

    def count(self):
        total = 0
        for range, rval in self.ranges:
            x1, x2 = range
            size = (x2 - x1) + 1
            if isinstance(rval, RangeMap):
                total += size * rval.count()
            else:
                total += size if rval else 0
        return total

    def draw(self, minx, maxx, join="\n"):
        grid = {}
        for r, rval in self.ranges:
            if isinstance(rval, RangeMap):
                drawn = rval.draw(minx, maxx, join="")
            else:
                drawn = str(rval)
            for x in range(r[0], r[1] + 1):
                grid[x] = drawn
        
        return join.join([grid.get(x, ".") for x in range(minx, maxx + 1)])

    def lines(self):
        lines = []
        for range, rval in self.ranges:
            if isinstance(rval, RangeMap):
                lines.append(f"{range}:")
                lines += [f"  {x}" for x in rval.lines()]
            else:
                lines.append(f"{range}: {rval}")
        return lines
    
    def __str__(self) -> str:
        return "\n".join(self.lines())

rmap = RangeMap()

with open("testinput") as f:
    input = f.read()

lines = [line.strip().split(" ") for line in input.strip().split("\n")]
lines = [[l[0], [[int(y) for y in x.split("=")[1].split("..")] for x in l[1].split(",")]] for l in lines]

def generator():
    alphabet = "XYZWUV"
    index = [0]
    def factory():
        value = alphabet[index[0]]
        index[0] += 1
        return value
    return factory
gen = generator()

for mode, ranges in lines:
    values = [*ranges, mode == "on"]
    rmap.add_range(values[0], values[1:])
    #print(rmap.count())
    #print(rmap)
    #print(rmap.draw(8, 14))
    #print("---")

print(rmap.count())