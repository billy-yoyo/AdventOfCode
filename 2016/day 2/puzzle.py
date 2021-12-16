
with open("input") as f:
    input = f.read()

keypad = [[None, None, 1, None, None], [None, 2, 3, 4, None], [5, 6, 7, 8, 9], [None, "A", "B", "C", None], [None, None, "D", None, None]]
pos = [0, 2]

def update(x, y):
    if 0 <= x < 5 and 0 <= y < 5 and keypad[y][x] is not None:
        pos[0] = x
        pos[1] = y

code = []
for line in input.strip().split("\n"):
    for c in line.strip():
        
        if c == "U":
            update(pos[0], pos[1] - 1)
        elif c == "D":
            update(pos[0], pos[1] + 1)
        elif c == "L":
            update(pos[0] - 1, pos[1])
        elif c == "R":
            update(pos[0] + 1, pos[1])
    print(pos)
    code.append(keypad[pos[1]][pos[0]])

print("".join(str(x) for x in code)) 