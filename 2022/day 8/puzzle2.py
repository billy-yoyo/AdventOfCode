
data = """
30373
25512
65332
33549
35390
""".strip()

with open("data") as f:
    data = f.read()

rows = [[int(x) for x in row] for row in data.split("\n")]
width = len(rows[0])
height = len(rows)

def visibility(x, y):
    tree = rows[y][x]
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    product = 1
    total = 0
    for dx, dy in directions:
        nx, ny = x, y
        while True:
            nx, ny = nx + dx, ny + dy
            if nx >= 0 and nx < width and ny >= 0 and ny < height:
                if rows[ny][nx] < tree:
                    total += 1
                else:
                    product *= (total + 1)
                    total = 0
                    break
            else:
                product *= total
                total = 0
                break
    return product

best_score = max(visibility(x, y) for x in range(width) for y in range(height))
print(best_score)
