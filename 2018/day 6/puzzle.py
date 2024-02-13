from collections import defaultdict

with open("input") as f:
    coords = [[int(x.strip()) for x in l.split(",")] for l in f.read().strip().split("\n")]

minx = min(x[0] for x in coords)
maxx = max(x[0] for x in coords)
miny = min(x[1] for x in coords)
maxy = max(x[1] for x in coords)

border_regions = set()
region_size = defaultdict(int)

central_region = 0

for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
        best_id, best_dist, collides = None, None, False
        for i, (cx, cy) in enumerate(coords):
            dist = abs(x - cx) + abs(y - cy)
            if best_dist is None or dist < best_dist:
                best_id, best_dist, collides = i, dist, False
            elif dist == best_dist:
                collides = True

        total_dist = sum(abs(x - cx) + abs(y - cy) for cx, cy in coords)
        if total_dist < 10_000:
            central_region += 1
            
        if not collides:
            region_size[best_id] += 1
            if x == minx or x == maxx or y == miny or y == maxy:
                border_regions |= {best_id}

#print(border_regions)
#print(region_size)

largest_finite_region = max(region_size[i] for i, _ in enumerate(coords) if i not in border_regions)
print(largest_finite_region)
print(central_region)