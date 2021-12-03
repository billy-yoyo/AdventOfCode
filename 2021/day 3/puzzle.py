

with open("input") as f:
    data = f.read()

rows = sorted(tuple(int(x) for x in line) for line in data.strip().split("\n"))

def find_first_1(rows, column, start, end):
    for i in range(start, end):
        if rows[i][column] == 1:
            return i
    return end

def find_new_top_bottom(rows, column, top, bottom, invert=True):
    mid = find_first_1(rows, column, top, bottom)
    if (invert and mid - top > bottom - mid) or (not invert and mid - top <= bottom - mid):
        bottom = mid
    else:
        top = mid
    return top, bottom

ox_top, ox_bottom = 0, len(rows)
co2_top, co2_bottom = 0, len(rows)
for i in range(len(rows[0])):
    ox_top, ox_bottom = find_new_top_bottom(rows, i, ox_top, ox_bottom)
    co2_top, co2_bottom = find_new_top_bottom(rows, i, co2_top, co2_bottom, invert=False)

def build_bits(bits):
    n = 0
    for i, bit in enumerate(bits[::-1]):
        n += bit << i
    return n

ox = build_bits(rows[ox_top])
co2 = build_bits(rows[co2_top])

print(ox * co2)