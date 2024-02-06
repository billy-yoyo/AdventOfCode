import math
from collections import defaultdict

with open("input") as f:
    data = f.read().strip().split("\n")

particles = []
for line in data:
    pstring, vstring, astring = line.strip().split(", ")
    position = [int(x.strip()) for x in pstring[3:-1].strip().split(",")]
    velocity = [int(x.strip()) for x in vstring[3:-1].strip().split(",")]
    acceleration = [int(x.strip()) for x in astring[3:-1].strip().split(",")]
    particles.append((position, velocity, acceleration))

def is_int(x):
    return abs(x - int(x)) < 0.00001

def axis_solutions(particle_1, particle_2, axis):
    x1, v1, a1 = [x[axis] for x in particle_1]
    x2, v2, a2 = [x[axis] for x in particle_2]

    a = a1 - a2

    if a == 0:
        divisor = v1 - v2
        if divisor == 0:
            return set()
        return {(x2 - x1) / divisor}

    b = (a1 - a2) + (2 * (v1 - v2))
    c = -2 * (x2 - x1)

    det = (b * b) - (4 * a * c)
    if det < 0:
        return set()
    elif det == 0:
        return {-b / (2 * a)}
    else:
        lhs = -2 / (2 * a)
        rhs = math.sqrt(det) / (2 * a)
        return {lhs + rhs, lhs - rhs}
    
def filtered_axis_solutions(particle_1, particle_2, axis):
    return {int(x) for x in axis_solutions(particle_1, particle_2, axis) if x >= 0 and is_int(x)}

def evaluate_at(particle, axis, t):
    x, v, a = [x[axis] for x in particle]
    return x + ((t * ((a * t) + a + (2 * v))) / 2)

def collide_at(particle_1, particle_2, t):
    position_1 = [evaluate_at(particle_1, i, t) for i in range(3)]
    position_2 = [evaluate_at(particle_2, i, t) for i in range(3)]
    return all(x == y for x, y in zip(position_1, position_2))

def solution_valid_for_axis(particle_1, particle_2, axis, solution):
    x1 = evaluate_at(particle_1, axis, solution)
    x2 = evaluate_at(particle_2, axis, solution)
    return abs(x1 - x2) < 0.00001


def find_solution(particle_1, particle_2):
    solns = set()
    for i in range(3):
        axis_solns = filtered_axis_solutions(particle_1, particle_2, i)
        if len(axis_solns) > len(solns):
            solns = axis_solns

    return {
        x for x in solns if all(solution_valid_for_axis(particle_1, particle_2, i, x) for i in range(3))
    }

def part2_stupid():
    collided = set()
    for t in range(50):
        collided_this_tick = set()
        for i, particle in enumerate(particles):
            if i in collided:
                continue
            for j in range(i):
                if j in collided:
                    continue
                if collide_at(particle, particles[j], t):
                    collided_this_tick |= {j, i}
        collided |= collided_this_tick
    
    print(len(particles) - len(collided))

def part2_smart():
    collisions = defaultdict(int)

    all_solns = set()
    for i, particle in enumerate(particles):
        for j in range(i):
            other_particle = particles[j]
            solns = find_solution(particle, other_particle)
            all_solns |= solns
            if len(solns) > 0:
                collisions[i] += 1
                collisions[j] += 1

    print(max(all_solns))

    total = 0
    for i, _ in enumerate(particles):
        if collisions[i] == 0:
            total += 1

    print(total)

part2_stupid()

#slowest_acc = min(particles, key=lambda x: sum(abs(a) for a in x[2]))
#print(slowest_acc)
#print(particles.index(slowest_acc))

