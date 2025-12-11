

data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()

with open("data") as f:
    data = f.read()

def dist(sx, sy, ex, ey):
    return abs(sx - ex) + abs(sy - ey)

def parse_sensor(line):
    left, right = line.split(": ")
    sensor_coords = left.split(" at ")[1].split(", ")
    sx, sy = [int(p.split("=")[1]) for p in sensor_coords]

    beacon_coords = right.split(" at ")[1].split(", ")
    bx, by = [int(p.split("=")[1]) for p in beacon_coords]

    return (sx, sy), (bx, by), dist(sx, sy, bx, by)

def within_sensor(x, y, sensor):
    s, b, sd = sensor
    d = dist(x, y, *s)
    return d <= sd and (x != b[0] or y != b[1])

sensors = [parse_sensor(line) for line in data.split("\n")]

min_x = min(min(s[0], b[0]) for s, b, _ in sensors)
max_x = max(max(s[0], b[0]) for s, b, _ in sensors)
min_y = min(min(s[1], b[1]) for s, b, _ in sensors)
max_y = max(max(s[1], b[1]) for s, b, _ in sensors)

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def len(self):
        return (self.end - self.start) + 1
    
    def exclude(self, range):
        if range.start <= self.start and self.end <= range.end:
            return []
        elif self.start <= range.start and range.end <= self.end:
            ranges = []
            if self.start < range.start:
                ranges.append(Range(self.start, range.start - 1))
            if range.end < self.end:
                ranges.append(Range(range.end + 1, self.end))
            return ranges
        elif self.start < range.start and self.end >= range.start:
            return [Range(self.start, range.start - 1)]
        elif self.start <= range.end and self.end > range.end:
            return [Range(range.end + 1, self.end)]
        else:
            return [self]

    def __str__(self) -> str:
        return f"[{self.start}, {self.end}]"

def add_range(ranges, range):
    range_set = [range]
    for range in ranges:
        new_range_set = []
        for subrange in range_set:
            new_range_set += subrange.exclude(range)
        range_set = new_range_set
    return range_set


size = 4_000_000

print(min_y, max_y)

y = 2000000
def find_beacon(y):
    ranges = []
    for s, _, d in sensors:
        pd = dist(s[0], y, *s)
        if pd <= d:
            xoff = (d - pd)
            ranges += add_range(ranges, Range(s[0] - xoff, s[0] + xoff))
    
    remainder = add_range(ranges, Range(0, size))
    if len(remainder) > 0:
        print(y)
        print(", ".join(str(r) for r in remainder))
        #return True

tx, ty = 3433501, 2908372
print((tx * size) + ty)

for y in range(2900000, size):
    if y % 100_000 == 0:
        print(y)
    if find_beacon(y):
        break



#total_range = sum(r.len() for r in ranges)
#print(total_range - len(total_beacons))
