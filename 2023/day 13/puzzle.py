
def smart_compare(flipped, i, left_slice, right_slice):
    if len(left_slice) != len(right_slice):
        return []
    
    errors = []
    for y, (left, right) in enumerate(zip(left_slice, right_slice)):
        for x, (lc, rc) in enumerate(zip(left, right)):
            if lc != rc:
                error = (x, i + 1 + y - len(left_slice))
                if flipped:
                    errors.append((error[1], error[0]))
                else:
                    errors.append(error)
                if len(errors) > 1:
                    return []
    return errors

def fix_size(x, y):
    size = min(len(x), len(y))
    return x[len(x)-size:], y[:size]

def find_mirror_points(pattern):
    for i, x in enumerate(pattern[:-1]):
        left_slice, right_slice = fix_size(pattern[:i+1], pattern[i+1:])
        #print(f"comparing at {i+1}:\n    {left_slice}\n    {list(reversed(right_slice))}")
        if left_slice == list(reversed(right_slice)):
            yield i + 1

def find_smudges_for_pattern(pattern, flipped):
    for i, x in enumerate(pattern[:-1]):
        left_slice, right_slice = fix_size(pattern[:i+1], pattern[i+1:])
        smudges = smart_compare(flipped, i, left_slice, list(reversed(right_slice)))
        if len(smudges) > 0:
            return smudges[0]
    return None

def find_all_mirrors_points(pattern, to_ignore):
    total = 0
    for x in find_mirror_points(pattern):
        p = (0, x)
        if p not in to_ignore:
            yield p
        total += x * 100
    
    columns = ["".join(pattern[i][x] for i in range(len(pattern))) for x in range(len(pattern[0]))]
    for x in find_mirror_points(columns):
        p = (x, 0)
        if p not in to_ignore:
            yield p

def count_mirror_points(pattern, to_ignore=None):
    total = 0
    for x, y in find_all_mirrors_points(pattern, to_ignore or []):
        total += x + (y * 100)
    return total

def flip(c):
    if c == "#":
        return "."
    else:
        return "#"

def fuzzy_find_mirrors(pattern):
    original_points = list(find_all_mirrors_points(pattern, []))

    columns = ["".join(pattern[i][x] for i in range(len(pattern))) for x in range(len(pattern[0]))]
    row_smudge = find_smudges_for_pattern(pattern, False)
    col_smudge = find_smudges_for_pattern(columns, True)

    sx, sy = row_smudge or col_smudge

    pattern[sy] = pattern[sy][:sx] + flip(pattern[sy][sx]) + pattern[sy][sx+1:]

    return count_mirror_points(pattern, original_points)


with open("input") as f:
    data = f.read().strip().split("\n\n")
    pt1_total = 0
    pt2_total = 0 
    for chunk in data:
        pattern = chunk.strip().split("\n")
        pt1_total += count_mirror_points(pattern)
        pt2_total += fuzzy_find_mirrors(pattern)
    print(pt1_total)
    print(pt2_total)
