from functools import cache

serial_number = 1133

def power_level(x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level //= 100
    power_level %= 10
    power_level -= 5
    return power_level

def find_subgrid():
    best_region = (0, 0, 0)
    best_region_power = 0
    for sx in range(300):
        for sy in range(300):
            region_power = 0
            for size in range(1, max(20, 20) + 1):
                region_power += power_level(sx + size - 1, sy + size - 1)
                for i in range(size - 1):
                    region_power += power_level(sx + size - 1, sy + i)
                    region_power += power_level(sx + i, sy + size - 1)
                if region_power > best_region_power:
                    best_region, best_region_power = (sx, sy, size), region_power
    return best_region, best_region_power

def recover_power(l1data, x, y):
    return l1data[y][x]

def shrink_data(l1data, data, size):
    best_region = (0, 0)
    best_region_power = 0
    for dy, row in enumerate(data[:-(size - 1)]):
        for dx, old_region_power in enumerate(row[:-(size - 1)]):
            region_power = old_region_power + recover_power(l1data, dx + size - 1, dy + size - 1)
            for i in range(size - 1):
                region_power += recover_power(l1data, dx + size - 1, dy + i)
                region_power += recover_power(l1data, dx + i, dy + size - 1)
            data[dy][dx] = region_power
            if region_power > best_region_power:
                best_region, best_region_power = (dx, dy), region_power
    return best_region, best_region_power

def find_all_subgrids():
    l1data = [[power_level(x, y) for x in range(300)] for y in range(300)]
    data = list(list(x) for x in l1data)
    best_region = (0, 0, 0)
    best_region_power = 0
    size = 1
    while size < 50:
        print(size)
        size += 1
        cregion, cregion_power = shrink_data(l1data, data, size)
        if cregion_power > best_region_power:
            best_region = (cregion[0], cregion[1], size)
            best_region_power = cregion_power
    return best_region, best_region_power

print(find_subgrid())

