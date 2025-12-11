
with open("input") as f:
    congruences = [
        ((-(i + 1 + int(parts[-1][:-1]))) % int(parts[3]), int(parts[3]))
        for i, parts in 
        enumerate([line.split(" ") for line in f.read().strip().split("\n")])
    ]

def euclidan(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - (quotient * r)
        old_s, s = s, old_s - (quotient * s)
        old_t, t = t, old_t - (quotient * t)
    
    return old_s, old_t 

def crt(bus1, bus2):
    a1, n1 = bus1
    a2, n2 = bus2

    m1, m2 = euclidan(n1, n2)

    return ((a1 * m2 * n2) + (a2 * m1 * n1)) % (n1 * n2), n1 * n2

solution = congruences[0]
for congruence in congruences[1:]:
    solution = crt(solution, congruence)

print(solution[0])
