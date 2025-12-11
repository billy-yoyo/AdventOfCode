
with open("input") as f:
    input = f.read()

old_triangles = [[int(x.strip()) for x in line.split(" ") if x.strip()] for line in input.strip().split("\n")]
triangles = []

for column in range(3):
    for i in range(0, len(old_triangles), 3):
        triangles.append([
            old_triangles[i][column],
            old_triangles[i + 1][column],
            old_triangles[i + 2][column]
        ])

def valid(tri):
    a, b, c = sorted(tri)
    return a + b > c

print(len([x for x in triangles if valid(x)]))
