


with open("input") as f:
    vectors = [
        [[int(x) for x in xs.strip().split(",")] for xs in l.strip().split("@")] for l in f.read().strip().split("\n")
    ]

MINI = 200000000000000
MAXI = 400000000000000

bounds = (
    (MINI, MAXI),
    (MINI, MAXI),
    None
)

INF = float("inf")

def solve(v1, v2):
    px1, py1, pz1 = v1[0]
    vx1, vy1, vz1 = v1[1]
    px2, py2, pz2 = v2[0]
    vx2, vy2, vz2 = v2[1]

    num = (vx1 * (py2 - py1)) - (vy1 * (px2 - px1))
    denom = (vx2 * vy1) - (vx1 * vy2)

    if denom == 0:
        if num == 0:
            L2 = 0
        else:
            return INF, INF, [INF, INF, INF]
    else:
        L2 = num / denom
    L1 = (
        (px2 - px1) + (L2 * vx2)
    ) / (
        vx1
    )

    return L1, L2, [
        px2 + (vx2 * L2),
        py2 + (vy2 * L2),
        pz2 + (vz2 * L2),
    ]

def in_bounds(p):
    for x, bound in zip(p, bounds):
        if bound is not None and (x < bound[0] or x > bound[1]):
            return False
    return True

n = 0

for i, v1 in enumerate(vectors):
    for j in range(i):
        coef1, coef2, collision = solve(v1, vectors[j])
        #print(f"Hailstone A: {v1}")
        #print(f"Hailstone B: {vectors[j]}")
        print(f"Collision at: {coef1}, {coef2}, {collision}")
        if coef1 >= 0 and coef2 >= 0 and in_bounds(collision):
            #print("    INSIDE!")
            n += 1
        #print("")

print(n)
