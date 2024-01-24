import numpy as np

with open("input") as f:
    vectors = [
        [np.array([int(x) for x in xs.strip().split(",")]) for xs in l.strip().split("@")] for l in f.read().strip().split("\n")
    ]


for i, vector in enumerate(vectors):
    p1, v1 = vector
    for j in range(i):
        p2, v2 = vectors[j]
        if (p1 == p2).all():
            print(f"found matching {p1},{v1} && {p2},{v2}")

