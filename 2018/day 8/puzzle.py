
def read_tree(pointer, numbers):
    n_children, n_metadata = numbers[pointer], numbers[pointer + 1]
    pointer += 2
    children = []
    for _ in range(n_children):
        pointer, child = read_tree(pointer, numbers)
        children.append(child)
    metadata = numbers[pointer:pointer+n_metadata]
    return pointer + n_metadata, (children, metadata)

def parse_tree(numbers):
    return read_tree(0, numbers)[1]

def count_metadata(tree):
    total = sum(tree[1])
    for child in tree[0]:
        total += count_metadata(child)
    return total

def node_value(node):
    children, metadata = node
    if len(children) == 0:
        return sum(metadata)
    else:
        return sum(node_value(children[x - 1]) for x in metadata if 0 <= x - 1 < len(children))

with open("input") as f:
    numbers = [int(x) for x in f.read().strip().split(" ")]

tree = parse_tree(numbers)

print(count_metadata(tree))
print(node_value(tree))
