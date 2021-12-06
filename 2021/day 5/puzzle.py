from collections import defaultdict

def parse_line(line):
    left, right = line.split(" -> ")
    left = [int(x) for x in left.split(",")]
    right = [int(x) for x in right.split(",")]
    return left, right

def parse_input(input):
    return [parse_line(line.strip()) for line in input.strip().split("\n") if line.strip()]

pos_map = defaultdict(int)

def write_point(x, y):
    pos_map[(x, y)] += 1

def write_line(line):
    left, right = line
    if left[0] == right[0]:
        for y in range(min(left[1], right[1]), max(left[1], right[1]) + 1):
            write_point(left[0], y)
    elif left[1] == right[1]:
        for x in range(min(left[0], right[0]), max(left[0], right[0]) + 1):
            write_point(x, left[1])
    else:
        minx, maxx = left[0], right[0]
        y0, y1 = left[1], right[1]

        if minx > maxx:
            minx, maxx = right[0], left[0]
            y0, y1 = right[1], left[1]
        
        dy = 1 if y0 < y1 else -1
        for i, x in enumerate(range(minx, maxx+1)):
            write_point(x, y0 + (dy * i))

with open("input") as f:
    input = f.read()

lines = parse_input(input)
for line in lines:
    write_line(line)

print(sum(v > 1 for v in pos_map.values()))
