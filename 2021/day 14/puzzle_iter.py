from collections import defaultdict
import time

start_time = time.time()
with open("testinput") as f:
    input = f.read()

start, rules = input.strip().split("\n\n")
rules = {x: y for x, y in [x.strip().split(" -> ") for x in rules.split("\n")]}

pair_counts = defaultdict(int)

for i in range(1, len(start)):
    pair_counts[start[(i-1):(i+1)]] += 1

def step(pair_counts):
    next_pair_counts = defaultdict(int)
    for pair, count in pair_counts.items():
        if pair in rules:
            middle = rules[pair]
            left, right = pair[0] + middle, middle + pair[1]
            next_pair_counts[left] += count
            next_pair_counts[right] += count
        else:
            next_pair_counts[pair] += count
    return next_pair_counts

for i in range(40):
    pair_counts = step(pair_counts)

counts = defaultdict(int)

for pair, count in pair_counts.items():
    counts[pair[0]] += count
    counts[pair[1]] += count

counts[start[0]] += 1
counts[start[-1]] += 1

mini = min(counts.values()) // 2
maxi = max(counts.values()) // 2

print(maxi - mini)

end_time = time.time()
print(f"Took {end_time - start_time} seconds")