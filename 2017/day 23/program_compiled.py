from functools import cache
import math

@cache
def is_prime(x):
    if x % 2 == 0:
        return False
    for i in range(3, math.ceil(math.sqrt(x)) + 1, 2):
        if x % i == 0:
            return False
    return True

@cache
def is_semiprime(x):
    if x % 2 == 0:
        return is_prime(x // 2)
    for i in range(3, math.floor(math.sqrt(x)), 2):
        if x % i == 0 and is_prime(x // i):
            return True
    return False

count = 0
for i in range(108100, 125101, 17):
    if not is_prime(i):
        count += 1

print(count)
