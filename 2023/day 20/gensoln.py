from functools import cache
import itertools

LOW = 1
HIGH = 2

with open("input") as f:
    lines = f.read().strip().split("\n")
    all_names = [x[1:] if x[0] in "&%" else x for x in [l.split(" -> ")[0].strip() for l in lines]]
    all_destinations = [l.split(" -> ")[1].strip().split(", ") for l in lines]
    all_inputs = [[input_name for i, input_name in enumerate(all_names) if name in all_destinations[i]] for name in all_names]
    all_functypes = [l.strip()[0] for l in lines]

    function_info = { name: (dests, inputs, functype) for name, dests, inputs, functype in zip(all_names, all_destinations, all_inputs, all_functypes) }

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

    return (a1 * m2 * n2) + (a2 * m1 * n1), n1 * n2

def period_of(name, value, visited):
    if name in visited:
        return []

    _, inputs, functype = function_info[name]
    if functype == "b":
        if value == LOW:
            return [(0, 1)]
        else:
            return []
    elif functype == "%":
        input_periods = [p for i in inputs for p in period_of(i, LOW, visited + [name])]
        #print(input_periods)
        if value == LOW:
            return [(o + p, 2 * p) for o, p in input_periods]
        else:
            return [(o, 2 * p) for o, p in input_periods]
    elif functype == "&":
        input_periods = [period_of(i, HIGH, visited + [name]) for i in inputs]
        print(input_periods)
        solutions = []
        for input_set in itertools.product(*input_periods):
            solution = input_set[0]
            for period in input_set[1:]:
                solution = crt(solution, period)
            solutions.append(solution)
        return solutions

rx_input = [x for x in function_info if "rx" in function_info[x][0]][0]
print(period_of(rx_input, LOW, []))
