import math
import sys
from functools import cache

target = 2900000

n = 0
v = 2
decomp = [0]
while n < target:
    n += v
    decomp[0] += 1
    v *= 2

primes = [2]
for x in range(3, math.ceil(math.sqrt(v)), 2):
    if all(x % prime != 0 for prime in primes):
        primes.append(x)

decomp += [0] * (len(primes) - 1)

def score(decomp, sub_decomp=None):
    n = 0
    for index, (prime, i) in enumerate(zip(primes, decomp)):
        if sub_decomp is not None and index < len(sub_decomp):
            i -= sub_decomp[index]

        v = prime
        for _ in range(i):
            n += v
            v *= prime
    return n

@cache
def calculate_decomp(n):
    index = 0
    n_sqrt = math.ceil(math.sqrt(n))
    for prime in primes:
        if prime >= n_sqrt:
            break
        index += 1

    decomp = [0] * index
    for i, x in enumerate(primes):
        if i >= len(decomp):
            break
        xp = x
        while n % xp == 0:
            decomp[i] += 1
            xp *= x
    return decomp

def iterate_subdecomps(prime):
    for n in range(prime - 1, 0, -1):
        yield calculate_decomp(n)

def can_afford(decomp, sub_decomp):
    return all(x <= decomp[i] for i, x in enumerate(sub_decomp))

def find_lowest_decomp(target):
    decomp = [0] * len(primes)
    n, v = 0, 2
    while n < target:
        n += v
        decomp[0] += 1
        v *= 2
    
    for i, prime in primes:
        # skip 2 since this is our initial decomposition
        if i == 0:
            continue
        
        for sub_decomp in iterate_subdecomps(prime):
            while can_afford(decomp, sub_decomp) and score(decomp, sub_decomp) > target:

    return decomp

print(len(primes))
print(len(decomp))"""