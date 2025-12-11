import numpy as np
import random

with open("input") as f:
    vectors = [
        [np.array([int(x) for x in xs.strip().split(",")]) for xs in l.strip().split("@")] for l in f.read().strip().split("\n")
    ]

MINI = 200000000000000
MAXI = 400000000000000
EPSILON = 0.00001

bounds = (
    (MINI, MAXI),
    (MINI, MAXI),
    (MINI, MAXI)
)

INF = float("inf")

def at(vector, t):
    p, v = vector
    return p + (v * t)



def cross(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return [
        (ay * bz) - (az * by),
        (az * bx) - (ax * bz),
        (ax * by) - (ay * bx)
    ]

def collides(p1, v1, p2, v2):
    cv = cross(v1, v2)
    pdiff = [a - b for a, b in zip(p1, p2)]
    total = sum(a * b for a, b in zip(cv, pdiff))
    return total <= EPSILON

def min_distance(a, b, c):
    d = (c - b) / np.linalg.norm(c - b)
    v = a - b
    t = v.dot(d)
    p = b + (t * d)
    return np.linalg.norm(p - a)



def in_bounds(p):
    for x, bound in zip(p, bounds):
        if bound is not None and (x < bound[0] or x > bound[1]):
            return False
    return True

def are_colinear(p1, p2, p3):
    return min_distance(p1, p2, p3) <= EPSILON

def collides(v1, v2):
    a, u = v1
    b, v = v2

    for i in range(3):
        if u[i] != v[i]:
            break
    else:
        return a == b

    t = (b[i] - a[i]) / (u[i] - v[i])

    for j in range(3):
        if i == j:
            continue
        if abs((a[j] + (t * u[j])) - (b[j] + (t * v[j]))) > EPSILON:
            return False

    return True


MIN_TIME = 1
MAX_TIME = 10000

def find_solutions(v1i, v2i, vectors, max_time):
    v1, v2 = vectors[v1i], vectors[v2i]
    v2_times = [at(v2, i) for i in range(1, max_time)]
    for i in range(1, max_time):
        p1 = at(v1, i)
        for j, p2 in enumerate(v2_times):
            if i == j:
                continue

            v = (p1 - p2) / (i - j)
            s = p1 - (i * v)
            vector = [s, v]

            for k, other_vector in enumerate(vectors):
                if k != v1i and k != v2i and not collides(vector, other_vector):
                    break
            else:
                print(f"solution with {vector}")
                return True

def find_solutions_second_method(vectors, max_time):
    for i, v1 in enumerate(vectors):
        for j in range(i):
            print(f"{i}, {j}")

            if find_solutions(i, j, vectors, max_time):
                return True
        

def single_axis_ticks(v, axis):
    x, dx = v[0][axis], v[1][axis]
    if dx > 0:
        return (MAXI - x) // dx
    else:
        return (x - MINI) // (-dx)

def count_ticks(v):
    return min(single_axis_ticks(v, i) for i in range(3))

#def find_solutions_third_method(vectors):

for v in vectors:
    print(count_ticks(v))

#find_solutions_second_method(vectors, 100)



