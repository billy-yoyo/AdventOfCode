import math

directions = "NESW"
direction_map = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0)
}
waypoint = (10, 1)
pos = (0, 0)

def read_line(line, waypoint, pos):
    wx, wy = waypoint
    x, y = pos

    ins, amount = line[0], int(line[1:])
    
    if ins in directions:
        dx, dy = direction_map[ins]
        # print(f"{line}: moving waypoint {ins} by {amount * dx}, {amount * dy}")
        return (wx + (amount * dx), wy + (amount * dy)), pos
    elif ins == "F":
        # print(f"{line}: moving towards waypoint by {amount}")
        return waypoint, (x + (wx * amount), y + (wy * amount))
    elif ins in "LR":
        dd = 1 if ins == "L" else -1
        
        cos, sin = math.cos(math.radians(dd * amount)), math.sin(math.radians(dd * amount))
        rwx = (wx * cos) - (wy * sin)
        rwy = (wx * sin) + (wy * cos)

        # print(f"{line}: rotating by {dd * amount}")

        return (rwx, rwy), pos
    else:
        raise ValueError(f"unknown ins {ins}")

with open("data") as f:
    for line in f.read().split():
        waypoint, pos = read_line(line, waypoint, pos)
        # print(f"waypoint={waypoint}, pos={pos}")

print(abs(pos[0]) + abs(pos[1]))