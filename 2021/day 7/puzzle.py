
with open("input") as f:
    input = f.read()
crabs = sorted([int(x) for x in input.strip().split(",")])

def fuel_cost(x):
    return x * (x + 1) / 2

def find_best_sum():
    i = 1
    last_sum = None
    while True:
        cur_sum = sum(fuel_cost(abs(x - i)) for x in crabs)
        if last_sum is not None and last_sum < cur_sum:
            return i - 1, last_sum
        last_sum = cur_sum
        i += 1

print(find_best_sum())

