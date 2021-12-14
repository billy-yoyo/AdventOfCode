from collections import defaultdict
import time

start_time = time.time()
with open("testinput") as f:
    input = f.read()

start, rules = input.strip().split("\n\n")
rules = {x: y for x, y in [x.strip().split(" -> ") for x in rules.split("\n")]}

cache = {}

def merge(d1, d2):
    for k, v in d2.items():
        d1[k] += v

def compute_element_pair(a, b, totals, steps):
    if steps == 0:
        return
    sub_totals = cache.get((a, b, steps), None)
    if sub_totals is None:
        sub_totals = defaultdict(int)
        if a + b in rules:
            c = rules[a + b]
            sub_totals[c] += 1
            compute_element_pair(a, c, sub_totals, steps - 1)
            compute_element_pair(c, b, sub_totals, steps - 1)
        cache[(a, b, steps)] = sub_totals
    merge(totals, sub_totals)

totals = defaultdict(int)
for c in start:
    totals[c] += 1

for i in range(1, len(start)):
    compute_element_pair(start[i-1], start[i], totals, 40)

mini = min(totals.values())
maxi = max(totals.values())

print(maxi - mini)

end_time = time.time()
print(f"Took {end_time - start_time} seconds")