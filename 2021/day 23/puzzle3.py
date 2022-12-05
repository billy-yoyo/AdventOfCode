
def counter():
    cache = [0]
    def count():
        cache[0] += 1
        return cache[0]
    return count
count = counter()


class Node:
    def __init__(self, target=None, values=None, max=1):
        self.target = target
        self.values = list(values) if values is not None else []
        self.max = max
        self.conns = []
        self.id = count()

    def success(self):
        return len(self.values) == self.max and all(v == self.target for v in self.values)

    def connect(self, node, steps):
        self.conns.append((node, steps))
        node.conns.append((self, steps))

    def iter_available(self, ignore_id, value, steps, must_be_room):
        if self.max == 1 and len(self.values) == 0:
            if not must_be_room:
                yield (self, steps)

            for node, step_cost in self.conns:
                if node.id != ignore_id:
                    yield from node.iter_available(self.id, value, steps + step_cost, must_be_room)
        elif self.max == 2 and len(self.values) < 2 and value == self.target:
            if len(self.values) == 1 and self.values[0] == self.target:
                yield (self, steps + 1)
            elif len(self.values) == 0:
                yield (self, steps)
    
    def find_movements(self):
        if len(self.values) > 0:
            steps = 0
            if self.max == 2:
                if self.success():
                    return
                if len(self.values) == 1 and self.values[0] == self.target:
                    return
                if len(self.values) == 1:
                    steps = 1
            for node, step_cost in self.conns:
                yield from node.iter_available(self.id, self.values[0], steps + step_cost, self.max == 1)
    
    def move_from(self):
        

    def __str__(self):
        return f"Node({self.id}, {self.target})"

rooms = [
    Node("A", "BA", max=2),
    Node("B", "CD", max=2),
    Node("C", "BC", max=2),
    Node("D", "DA", max=2)
]

spaces = [Node(), Node(), Node(), Node(), Node(), Node(), Node()]
for i, space in enumerate(spaces[:-1]):
    space.connect(spaces[i+1], 1 if i == 0 or i == len(spaces) - 1 else 2)

for i, room in enumerate(rooms):
    room.connect(spaces[i + 1], 2)
    room.connect(spaces[i + 2], 2)

nodes = rooms + spaces
value_map = {
    "A": 1, "B": 10, "C": 100, "D": 1000
}

class Best:
    def __init__(self):
        self.score = None

best = Best()

def play(score=0):
    if best.score is not None and score >= best.score:
        return

    if all(room.success() for room in rooms):
        print(f"found new best score {score}")
        best.score = score

    for node in nodes:
        for new_node, steps in node.find_movements():
            value = node.values[0]
            node.values[0] = None
            
            #print(f"moving {value} from {node} to {new_node}")
            play(score + (steps * value_map[value]))
            node.values.insert(0, new_node.values.pop(0))

play()