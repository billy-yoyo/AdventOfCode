import numpy as np
import random
import fractions

with open("example") as f:
    vectors = [
        [np.array([int(x) for x in xs.strip().split(",")]) for xs in l.strip().split("@")] for l in f.read().strip().split("\n")
    ]

MINI = 200000000000000
MAXI = 400000000000000
EPSILON = 0.00001

def eq1_coefs(vector1, vector2):
    p1, v1 = vector1
    p1x, p1y, _ = p1
    v1x, v1y, _ = v1

    p2, v2 = vector2
    p2x, p2y, _ = p2
    v2x, v2y, _ = v2

    return np.array([
        p2y - p1y,
        v1y - v2y,
        p1x - p2x,
        v2x - v1x,
        (p1x * v1y) - (p2x * v2y) - (p1y * v1x) + (p2y * v2x)
    ])

def create_system(vs):
    system = []
    for i in range(2):
        j = i + 1
        (pi, vi), (pj, vj) = vs[i], vs[j]
        for a0, a1 in [(1, 0), (1, 2), (2, 0)]:
            row = [0, 0, 0, 0, 0, 0, (
                (pi[a1] * vi[a0]) + (pj[a0] * vj[a1])
                - ((pi[a0] * vi[a1]) + (pj[a1] * vj[a0]))
            )]
            row[a0] = vj[a1] - vi[a1]
            row[a1] = vj[a0] - vi[a0]
            
            row[3 + a0] = pj[a1] - pi[a1]
            row[3 + a1] = pj[a0] - pi[a0]
            system.append(row)
    return system

def gauss(matrix):
    n = len(matrix)
    for i in range(n):
        i_pivot = i
        pivot = matrix[i_pivot][i]
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > pivot:
                pivot = matrix[j][i]
                i_pivot = j
        if matrix[i][i_pivot] == 0:
            return True
        for j in range(n + 1):
            matrix[i][j], matrix[i_pivot][j] = matrix[i_pivot][j], matrix[i][j]
        for j in range(i + 1, n):
            ratio = matrix[j][i] / matrix[i][i]
            for k in range(i + 1, n + 1):
                matrix[j][k] -= matrix[i][k] * ratio
            matrix[j][i] = 0

def back_substitute(matrix):
    n = len(matrix)
    x = [None for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (
            matrix[i][n] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))
        ) / matrix[i][i]
    return x

def solve(vs):
    matrix = create_system(vs)
    for row in matrix:
        for i, el in enumerate(row):
            row[i] = fractions.Fraction(el)
    if gauss(matrix):
        return
    return back_substitute((matrix))

def solve_system(v1, v2, v3, v4):
    c1, c2, c3, c4 = [
        eq1_coefs(v1, v2),
        eq1_coefs(v2, v3),
        eq1_coefs(v3, v4),
        eq1_coefs(v4, v1),
    ]

    c1 = c1 / c1[0]
    c2 = c2 / c2[0]
    c3 = c3 / c3[0]
    c4 = c4 / c4[0]

    c2 -= c1
    c3 -= c1
    c4 -= c1

    c2 = c2 / c2[1]
    c3 = c3 / c3[1]
    c4 = c4 / c4[1]

    c3 -= c2
    c4 -= c2
    
    c3 = c3 / c3[2]
    c4 = c4 / c4[2]

    c4 -= c3

    s4 = c4[4] / c4[3]
    s3 = c3[4] - (c3[3] * s4)
    s2 = c2[4] - ((c2[3] * s4) + (c2[2] * s3))
    s1 = c1[4] - ((c1[3] * s4) + (c1[2] * s3) + (c1[1] * s2))

    print(s1, s2, s3, s4)

solution = None
while solution is None:
    random.shuffle(vectors)
    solution = solve([vectors[0], vectors[1], vectors[2]])
print(sum(solution[:3]))

#solve_system(vectors[0], v
