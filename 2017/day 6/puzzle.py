


def redistribute(blocks):
    total = max(blocks)
    index = blocks.index(total)
    wraps = total // len(blocks)
    remainder = total % len(blocks)
    return tuple(
        (0 if i == index else x) + wraps + (((i - (index + 1)) % len(blocks)) < remainder)
        for i, x in enumerate(blocks)
    )

def cycle_length(blocks):
    visited = {}
    steps = 0
    while blocks not in visited:
        visited[blocks] = steps
        steps += 1
        blocks = redistribute(blocks)
    return steps - visited[blocks]
    
with open("input") as f:
    blocks = tuple(int(x) for x in f.read().strip().split())

#blocks = (0, 2, 7, 0)
print(cycle_length(blocks))
