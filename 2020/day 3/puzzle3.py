

with open("m", "r") as f:
    lines = [line.strip() for line in f]


def check_slope(dx, dy):
    x, y, trees = 0, 0, 0
    while y < len(lines):
        line = lines[y]
        if line[x % len(line)] == "#":
            trees += 1

        x += dx
        y += dy
    return trees

total_prod = 1
for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    trees = check_slope(*slope)
    print(f"slope {slope} encounters {trees} trees")
    total_prod *= trees

print(f"total product: {total_prod}")