from collections import defaultdict

with open("testinput") as f:
    input = f.read()

grid = defaultdict(bool)

people = []
for y, line in enumerate(input.strip().split("\n")):
    for x, char in enumerate(line.strip()):
        if char == ".":
            grid[(x, y)] = True
        elif char in "ABCD":
            people.append((x, y, char))

targets = people[:]
sorted_xs = sorted(set(pos[1] for pos in targets))
letters = "ABCD"
x_map = { x: letters[i] for i, x in enumerate(sorted_xs) }
target_map = { pos: x_map[pos[1]] for pos in targets }
score_map = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}
score_limit = 10000

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def can_move(pos):
    return any(grid[(pos[0] + dx, pos[1] + dy)] for dx, dy in dirs)

def move(from_pos, to_pos):
    grid[(from_pos[0], from_pos[1])] = True
    grid[(to_pos[0], to_pos[1])] = False

class Best:
    def __init__(self):
        self.cost = None

best = Best()

cache = defaultdict(bool)

def play(people, score=0):
    # cost is too high, elimate branch
    if score > score_limit or (best.cost is not None and score > best.cost):
        return

    people_hash = tuple(sorted(people))
    if cache[people_hash]:
        return

    if all((pos[0], pos[1]) in target_map and target_map[(pos[0], pos[1])] == pos[2] for pos in people):
        if best.cost is None or score < best.cost:
            best.cost = score
            print(f"found score {score}")

    cache[people_hash] = True

    for i, pos in enumerate(people):
        for dx, dy in dirs:
            to_pos = (pos[0] + dx, pos[1] + dy, pos[2])
            if grid[(pos[0] + dx, pos[1] + dy)]:
                move(pos, to_pos)
                play(people[:i] + [to_pos] + people[i + 1:], score=score + score_map[pos[2]])
                move(to_pos, pos)

    del cache[people_hash] 

play(people)

print(best.cost)