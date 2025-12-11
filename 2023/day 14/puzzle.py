import functools
import time

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def transpose(rows):
    return ["".join(row[x] for row in rows) for x in range(len(rows[0]))]

def reverse(rows):
    return [row[::-1] for row in rows]

def tilt_west(rows):
    new_rows = []
    for row in rows:
        new_row = []
        start = 0
        rolling_count = 0
        for x, c in enumerate(row):
            if c == "#":
                if start != x:
                    new_row.append(("O" * rolling_count) + ("." * ((x - start) - rolling_count)))
                new_row.append("#")
                start = x + 1
                rolling_count = 0
            elif c == "O":
                rolling_count += 1
        if start != len(row):
            new_row.append(("O" * rolling_count) + ("." * ((len(row) - start) - rolling_count)))
        new_rows.append("".join(new_row))
    return new_rows

@functools.cache
def tilt(rows, direction):
    if direction == NORTH:
        rows = transpose(rows)
    elif direction == EAST:
        rows = reverse(rows)
    elif direction == SOUTH:
        rows = transpose(rows)
        rows = reverse(rows)
    
    rows = tilt_west(rows)

    if direction == NORTH:
        rows = transpose(rows)
    elif direction == EAST:
        rows = reverse(rows)
    elif direction == SOUTH:
        rows = reverse(rows)
        rows = transpose(rows)
    
    return rows

def count_north_load(rows):
    height = len(rows)
    total = 0
    for i, row in enumerate(rows):
        total += (height - i) * row.count("O")
    return total

def cycle(rows):
    rows = tilt(tuple(rows), NORTH)
    rows = tilt(tuple(rows), WEST)
    rows = tilt(tuple(rows), SOUTH)
    rows = tilt(tuple(rows), EAST)
    return rows


start = time.time()
with open("input") as f:
    rows = f.read().strip().split("\n")
    initial_rows = rows
    
    cache = []

    offset = None
    cycle_size = None

    total = 1000000000
    for i in range(total):
        last_cycle = rows
        rows = cycle(rows)
        rows_hash = hash("".join(rows))
        try:
            last_entry = cache.index(rows_hash)
            if offset is None:
                offset = last_entry
            elif offset == last_entry:
                cycle_size = i - offset
                break
        except:
            pass
        cache.append(rows_hash)
    
    print(f"found cycle at offset {offset}, with size {cycle_size}")
    final_index = (total - offset) % cycle_size
    print(f"final index is {final_index}")

    rows = initial_rows
    for i in range(final_index + offset):
        rows = cycle(rows)

    print(count_north_load(tilt(tuple(initial_rows), NORTH)))
    print(count_north_load(rows))


end = time.time()
print(f"took {end - start}")