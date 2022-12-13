import json
from functools import cmp_to_key

with open("data") as f:
    data = f.read()

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1
    else:
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]

        for i, x in enumerate(left):
            if i >= len(right):
                return 1
            else:
                comparison = compare(x, right[i])
                if comparison != 0:
                    return comparison
        if len(left) < len(right):
            return -1
        else:
            return 0

pairs = [pair.split("\n") for pair in data.split("\n\n")]
pairs = [[json.loads(left), json.loads(right)] for left, right in pairs]

# part 1
total = sum(i for i, pair in enumerate(pairs) if compare(*pair) <= 0)
print(total)

# part 2
packets = [item for pair in pairs for item in pair]
packets += [ [[2]], [[6]] ]

packets = sorted(packets, key=cmp_to_key(compare))

div_1 = packets.index([[2]]) + 1
div_2 = packets.index([[6]]) + 1
print(div_1 * div_2)
