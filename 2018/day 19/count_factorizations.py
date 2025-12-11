import math

def factorizations(n):
    factors = 0
    for f in range(1, math.floor(math.sqrt(n)) + 1):
        if n % f == 0:
            factors += f + (n // f)
    return factors

def main(d):
    f = 1
    a = 0
    while f <= d:
        c = 1
        while c <= d:
            if f * c == d:
                a += f
            c += 1
        f += 1
    return a

print(factorizations(10551348))
#print(main(948))
