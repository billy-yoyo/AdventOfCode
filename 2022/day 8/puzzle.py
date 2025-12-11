from collections import defaultdict

data = """
30373
25512
65332
33549
35390
""".strip()

#with open("data") as f:
#    data = f.read()

rows = data.split("\n")
rows = [[int(x) for x in row] for row in rows]
columns = [[rows[j][i] for j in range(len(rows[0]))] for i in range(len(rows))]

visible = defaultdict(int)

for y, row in enumerate(rows):
    last = -1
    for x, val in enumerate(row):
        if val > last:
            visible[(x, y)] += x
            last = val
        
    
    last = -1
    for x, val in reversed(list(enumerate(row))):
        if val > last:
            visible[(x, y)] += len(row) - (x + 1)
            last = val

for x, col in enumerate(columns):
    last = -1
    for y, val in enumerate(col):
        if val > last:
            visible[(x, y)] += y
            last = val
    
    last = -1
    for y, val in reversed(list(enumerate(col))):
        if val > last:
            visible[(x, y)] += len(col) - (y + 1)
            last = val

print(max(visible.items(), key=lambda i: i[1]))

print(len(visible))
row_visible = "\n".join("".join("." if (x, y) in visible else "x" for x, c in enumerate(row)) for y, row in enumerate(rows))
#print(row_visible)