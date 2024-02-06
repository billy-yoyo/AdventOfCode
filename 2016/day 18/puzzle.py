
def is_trap(row, i):
    slice = "".join([
        row[i - 1] if i > 0 else ".",
        row[i],
        row[i + 1] if i < len(row) - 1 else "."
    ])
    return slice == "^^." or slice == ".^^" or slice == "^.." or slice == "..^"

def count_safe(initial_row, steps):
    row = initial_row
    safe = initial_row.count(".")
    for _ in range(steps - 1):
        row = [
            "^" if is_trap(row, i) else "." for i, _ in enumerate(row)
        ]
        safe += row.count(".")
    return safe

print(count_safe("^^.^..^.....^..^..^^...^^.^....^^^.^.^^....^.^^^...^^^^.^^^^.^..^^^^.^^.^.^.^.^.^^...^^..^^^..^.^^^^", 400000))
