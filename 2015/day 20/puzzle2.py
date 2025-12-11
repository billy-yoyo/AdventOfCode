import math
import json
import os

target = 29000000

def count_presents(x):
    n = x * 10
    for i in range(1, (x // 2) + 1):
        if x % i == 0:
            n += i * 10
    return n

def decompose(x):
    components = []
    for i in range(1, (x // 2) + 1):
        if x % i == 0:
            components.append(i)
    components.append(x)
    return components

def decompose_diff(x, y):
    xset = set(decompose(x))
    yset = set(decompose(y))
    return list((xset - yset) | (yset - xset))

def prime_decompose(x):
    primes = []
    decomposition = []
    for i in range(2, math.floor(math.sqrt(x)) + 1):
        is_prime = all(i % p != 0 for p in primes)
        if is_prime:
            primes.append(i)
            while x % i == 0:
                x = x // i
                decomposition.append(i)
    return decomposition

def print_table(columns):
    columns = [[str(x) for x in c] for c in columns]
    widths = [max(len(x) for x in c) for c in columns]
    for row in range(len(columns[0])):
        print("| ", end="")
        for c, w in zip(columns, widths):
            item = c[row]
            print(item + (" " * (w - len(item))), end = " | ")
        print("")

def diff(x, y):
    col = lambda i: [i, count_presents(i), prime_decompose(i), decompose(i), decompose_diff(x, y)]

    print_table([col(x), col(y)])
    
def extract_power(x, p):
    i = 1
    while x % p == 0:
        x //= p
        i *= p
    return i    

def estimate(x, y):
    diff(x, x * y)
    xp = count_presents(x)
    z = x * y

    est = 0
    if x % y != 0:
        est += xp * (y + 1)
    else:
        yp = extract_power(x, y) * y
        print(yp)
        print(set(prime_decompose(x)))
        for p in set(prime_decompose(x)) | {1}:
            est += p * yp * 10

    print(f"real: {count_presents(z)}")
    print(f" est: {est}")

#estimate(2 * 2 * 3 * 5, 5)

class Decomp:
    def __init__(self, x):
        self.x = x
        self.decomposition = decompose(x)
        self.presents = count_presents(x)
    
    def add_prime(self, y):
        yp = extract_power(self.x, y) * y
        for d in self.decomposition:
            if d % y != 0:
                self.decomposition.append(d * yp)
                self.presents += d * yp * 10
        self.x *= y

    def remove_prime(self, y):
        yp = extract_power(self.x, y)
        if yp > 1:
            old_decomposition = self.decomposition
            self.decomposition = []
            for d in old_decomposition:
                if d % yp == 0:
                    self.presents -= d * 10
                else:
                    self.decomposition.append(d)
        self.x //= y

    def check(self):
        print(f"{self.x}: {self.presents} == {count_presents(self.x)} // {self.decomposition}")

"""
x = Decomp(2)
primes = [2]

while x.presents < target:
    np = primes[-1] + 1
    # find the next prime
    while any(np % p == 0 for p in primes):
        np += 1
    primes.append(np)
    x.add_prime(np)
    
print(x.x)
print(x.decomposition)
print(primes)
print(x.presents)
"""

def get_max_power(p):
    n = 0
    x = 1
    i = 0
    while n < target:
        n += x * 10
        x *= p
        i += 1
    return i - 1

primes = [2, 3, 5, 7, 11, 13, 17, 19]
max_powers = [20, 13, 9, 7, 6, 5, 5, 5]

def iterate_numbers(index):
    if index >= len(primes):
        yield 1
    else:
        p = primes[index]
        pi = 1
        for pi in range(1, max_powers[index] + 1):
            for n in iterate_numbers(index + 1):
                if pi * n < target:
                    yield pi * n
            pi *= p
"""
batch_n = 0
batch = []
for x in iterate_numbers(0):
    batch.append(x)
    if len(batch) >= 100000:
        with open(f"batches/batch_{batch_n}.json", "w") as f:
            json.dump(batch, f)
        batch = []
        batch_n += 1

with open(f"batches/batch_{batch_n}.json", "w") as f:
    json.dump(batch, f)
"""

def process_next_batch():
    i = 0
    while os.path.exists(f"batches/batch_{i}.json") and os.path.exists(f"processed/processed_{i}.json"):
        i += 1
    if os.path.exists(f"batches/batch_{i}.json"):
        # create dummy file
        with open(f"processed/processed_{i}.json", "w") as f:
            json.dump([], f)
        
        with open(f"batches/batch_{i}.json", "r") as f:
            batch = json.load(f)

        processed = []
        for x in batch:
            presents = count_presents(x)
            if presents >= target and presents < 41943030:
                processed.append([x, presents])
        
        with open(f"processed/processed_{i}.json", "w") as f:
            json.dump(processed, f)

        print(f"found {len(processed)} candidates in batch {i}")
        return True
    else:
        print("no batches left to process!")
    return False

#while process_next_batch():
#    pass
"""
all_processed = []
i = 0
while os.path.exists(f"processed/processed_{i}.json"):
    with open(f"processed/processed_{i}.json", "r") as f:
        processed = json.load(f)
    all_processed += processed
    i += 1

x, presents = min(all_processed, key=lambda p: p[0])
print(x, presents)

print(count_presents(x))
print(prime_decompose(x))
print(decompose(x))

"""
#x = 2 * 2 * 3 * 3 * 3 * 5 * 7 * 7 * 23
#print(count_presents(x))

from collections import defaultdict

houses = defaultdict(int)
for i in range(1, target // 10):
    for j in range(i, min(target // 10, i * 51), i):
        houses[j] += i * 11

x, presents = 0, 0
for h, p in houses.items():
    if p >= target and (x == 0 or h < x):
        x, presents = h, p
print(x, presents)

#print(count_presents(2 * 2 * 3 * 5 * 7 * 11 * 13 * 17))

#print(decompose(2 * 3), " -> ", count_presents(2 * 3))
#print(decompose(2 * 2 * 3), " -> ", count_presents(2 * 2 * 3))

"""
print(decompose(2 * 2 * 3))
print(count_presents((2 ** 7) * (3 ** 3) * (5 ** 2) * 7))

n = 0
x = 1
while n < 29000000:
    n += x * 10
    x *= 2
x //= 2

print(x)
print(n)
41943030
29000000
25382800
26214000
345600
20971510"""
"""
x, count = max(((i, count_presents(i)) for i in range(10000000, 10001000)), key=lambda x: x[1])
print(x)
print(count)
print(prime_decompose(x))
print(decompose(x))"""