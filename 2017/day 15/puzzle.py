
factors = (16807, 48271)
starts = 289, 629

period = 2147483647

upper_bound = 65536

total = 40_000_000
#total = 6

found = set()

def num_generator(start, factor, validator):
    current = start
    for _ in range(total):
        current *= factor
        current %= period
        if current % validator == 0:
            yield current

def part1():
    results = 0
    current_a, current_b = starts
    for _ in range(total):
        current_a *= factors[0]
        current_b *= factors[1]


        current_a %= period
        current_b %= period

        if current_a % upper_bound == current_b % upper_bound:
            results += 1

    print(results)

def part2():
    a_gen = num_generator(starts[0], factors[0], 4)
    b_gen = num_generator(starts[1], factors[1], 8)
    results = 0
    for a, b in zip(a_gen, b_gen):
        if a % upper_bound == b % upper_bound:
            results += 1
    print(results)

part2()