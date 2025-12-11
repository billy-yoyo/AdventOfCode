
horz_lines = []
vert_lines = []

with open("example") as f:
    for line in f.read().strip().split("\n"):
        a, b = [v.strip() for v in line.split(",")]
        if a.startswith("x"):
            x, y = a[2:], b[2:]
        else:
            x, y = b[2:], a[2:]
        if ".." in x:
            sx, ex = [int(a) for a in x.split("..")]
            horz_lines.append(((sx, ex), int(y)))
        else:
            sy, ey = [int(a) for a in y.split("..")]
            vert_lines.append((int(x), (sy, ey)))

maximum_y = max(
    max(y for _, y in horz_lines),
    max(ey for _, (_, ey) in vert_lines)
)

def find_highest_vertical_collision(x, y):
    collision = None
    for lx, (sy, ey) in vert_lines:
        if lx == x and y < sy and (collision is None or sy < collision):
            collision = sy
    
    for (sx, ex), ly in horz_lines:
        if sx <= x <= ex and y < ly and (collision is None or ly < collision):
            collision = ly
    return collision

def find_left_right_collisions(x, y):
    left_collision, right_collision = None, None
    for lx, (sy, ey) in vert_lines:
        if sy <= y <= ey:
            if x < lx and (right_collision is None or lx < right_collision):
                right_collision = lx
            elif lx < x and (left_collision is None or lx > left_collision):
                left_collision = lx
    
    for (sx, ex), ly in horz_lines:
        if y == ly:
            if x < sx and (right_collision is None or sx < right_collision):
                right_collision = sx
            elif ex < x and (left_collision is None or ex > left_collision):
                left_collision = ex
    return left_collision, right_collision

def is_grounded(x, y, last_left, last_right):
    if last_left is not None and last_right is not None:
        if last_left <= x <= last_right:
            return True 
    return find_highest_vertical_collision(x, y) == y + 1
    

def count_water(sx, sy):
    water = 0
    x, y = sx, sy
    flow_y = find_highest_vertical_collision(x, y)

    # count to the bottom of the map
    if flow_y is None:
        return maximum_y - sy

    print(f"{(flow_y - (sy + 1))} water from spout starting at {sx},{sy}")
    water += (flow_y - (sy + 1))
    flow_y -= 1
    
    last_left, last_right = None, None
    left, right = find_left_right_collisions(x, flow_y)
    left_spout, right_spout = None, None
    while left_spout is None and right_spout is None and left is not None and right is not None:
        for cx in range(x - 1, left, -1):
            if is_grounded(cx, flow_y, last_left, last_right):
                water += 1
            else:
                left_spout = cx
                break

        for cx in range(x + 1, right):
            if is_grounded(cx, flow_y, last_left, last_right):
                water += 1
            else:
                right_spout = cx
                break
        
        last_left, last_right = left, right
        flow_y -= 1
        left, right = find_left_right_collisions(x, flow_y)

    if left_spout is None and left is None:
        nx = x - 1
        while is_grounded(nx, flow_y, last_left, last_right):
            nx -= 1
            water += 1
        left_spout = nx
    if right_spout is None and right is None:
        nx = x + 1
        while is_grounded(nx, flow_y, last_left, last_right):
            nx += 1
            water += 1
        water += count_water(nx, flow_y) + 1
        right_spout = nx
    
    print(f"y={flow_y} {left_spout=} {right_spout=}")

    if left_spout is None:
        print(f"left-terminus from {x},{flow_y} produced {x - (left + 1)} more water")
        water += x - (left + 1)
    else:
        water += count_water(left_spout, flow_y)

    if right_spout is None:
        print(f"right-terminus from {x},{flow_y} produced {x - (right + 1)} more water")
        water += right - (x + 1)
    else:
        water += count_water(right_spout, flow_y)
    
    return water

print(count_water(500, 0))
