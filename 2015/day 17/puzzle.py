
with open("data") as f:
    sizes = [int(line.strip()) for line in f]

target = 150

def iterate_ways(index=0, size=0, used=None):
    if used is None:
        used = []

    if size == target:
        yield used

    if index < len(sizes) and size < target:
        cur_size = sizes[index]

        yield from iterate_ways(index=index+1, size=size+cur_size, used=used+[index])
        yield from iterate_ways(index=index+1, size=size, used=used)

min_containers = len(min(iterate_ways(), key=lambda v: len(v)))
n_min_container = sum(len(used) == min_containers for used in iterate_ways())
print(n_min_container)