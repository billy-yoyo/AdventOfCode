
count_cache = [0]
def counter():
    count_cache[0] += 1
    return count_cache[0]

def get_score(value):
    return {
        "A": 1, "B": 10, "C": 100, "D": 1000
    }[value]

class StackNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent

class Stack:
    def __init__(self, values):
        self.tail = None
        if len(values):
            self.tail = StackNode(values[0])
            for value in values[1:]:
                self.tail = StackNode(value, self.tail)
        self.length = len(values)
        self.hash = tuple(values)
    
    def peek(self):
        if self.tail is None:
            return None
        else:
            return self.tail.value
    
    def pop(self):
        if self.tail is None:
            return None
        value = self.tail.value
        self.tail = self.tail.parent
        self.length -= 1
        self.hash = tuple(self.hash[:-1])
        return value

    def push(self, value):
        self.tail = StackNode(value, self.tail)
        self.hash = self.hash + (value,)
        self.length += 1

    def is_empty(self):
        return self.tail is None
    
    def is_full(self):
        return self.tail is not None

    def get(self, index):
        node = self.tail
        while node is not None and index > 0:
            node = node.parent
            index -= 1
        if node is None:
            return None
        else:
            return node.value

    def __iter__(self):
        node = self.tail
        while node is not None:
            yield node.value
            node = node.parent

    def __len__(self):
        return self.length
        

class Node:
    def __init__(self, room_target=None, values=None):
        self.id = counter()
        self.is_room = room_target is not None
        self.room_target = room_target
        self.connections = []
        self.values = Stack(list(values)[::-1] if values is not None else [])

    def connect(self, node, length):
        self.connections.append((node, length))
        node.connections.append((self, length))

    def path_to(self, target, length=0, last=None, first=False):
        if self.room_target == target:
            # can't move into a full room
            if len(self.values) >= 2:
                return None
            # only move into a room if it's empty, or if the existing value matches the target
            elif self.values.peek() is None or self.values.peek() == self.room_target:
                return self, (length + (1 - len(self.values)))
            else:
                return
        elif self.is_room:
            return None
        elif not first and not self.is_room and self.values.is_full():
            return None
            
        for conn, conn_length in self.connections:
            if last is None or last.id != conn.id:
                result = conn.path_to(target, last=self, length=length+conn_length)
                if result is not None:
                    return result
        
        return None
    
    def finished(self):
        return len(self.values) == 2 and all(v == self.room_target for v in self.values)
    
    def hallways(self, length=0, last=None, first=False):
        if not self.is_room:
            # this path is blocked
            if self.values.is_full():
                return
            yield self, length
        elif not first and self.is_room:
            return

        if first:
            left, right = self.connections
            yield from left[0].hallways(last=right[0], length=left[1])
            yield from right[0].hallways(last=left[0], length=right[1])
        else:
            for conn, conn_length in self.connections:
                if last is None or last.id != conn.id:
                    yield from conn.hallways(last=self, length=length+conn_length)
    
    def valid_moves(self, last=None):
        if self.values.is_full():
            step_cost = get_score(self.values.peek())
            if self.is_room:
                # this room is complete, or partially complete, so don't move out of it
                if all(v == self.room_target for v in self.values):
                    return
                else:
                    room_cost = 2 - len(self.values)
                    for dest, length in self.hallways(first=True):
                        yield dest, (length + room_cost) * step_cost
            else:
                # can we move to our room?
                result = self.path_to(self.values.peek(), first=True)
                if result is not None:
                    dest, length = result
                    yield dest, length * step_cost

    def move(self, to_node):
        value = self.values.pop()
        to_node.values.push(value)

    def get(self, index):
        value = None
        if self.is_room:
            if len(self.values) == 2:
                value = self.values.get(index)
            elif len(self.values) == 1:
                if index == 0:
                    return "."
                else:
                    return self.values.get(0)
        else:
            value = self.values.get(index)
        return value if value is not None else "."

    def __hash__(self) -> int:
        return hash(self.values.hash)


rooms = [
    Node("A", "DC"), Node("B", "BA"), Node("C", "CD"), Node("D", "AB")
]

hallway = [
    Node(), Node(), Node(), Node(), Node(), Node(), Node()
]

nodes = tuple(rooms + hallway)
nodemap = {node.id: node for node in nodes}

def game_string():
    return f"""
#############
#{hallway[0].get(0)}{hallway[1].get(0)}.{hallway[2].get(0)}.{hallway[3].get(0)}.{hallway[4].get(0)}.{hallway[5].get(0)}{hallway[6].get(0)}#
###{rooms[0].get(0)}#{rooms[1].get(0)}#{rooms[2].get(0)}#{rooms[3].get(0)}###
  #{rooms[0].get(1)}#{rooms[1].get(1)}#{rooms[2].get(1)}#{rooms[3].get(1)}#
  #########
    """.strip()
    
def print_game():
    print(game_string())

last_node = hallway[0]
for i, node in enumerate(hallway[1:]):
    node.connect(last_node, 1 if i == 0 or i == len(hallway) - 2 else 2)
    last_node = node

for i, room in enumerate(rooms):
    room.connect(hallway[i + 1], 2)
    room.connect(hallway[i + 2], 2)

best_soln = None

cache = {}

def find_solutions():
    cur_hash = hash(nodes)

    if cur_hash in cache:
        return cache[cur_hash]
    else:
        best_score = None
        if all(room.finished() for room in rooms):
            best_score = 0
        else:
            for node in nodes:
                for dest, cost in node.valid_moves():
                    node.move(dest)
                    sub_best_score = find_solutions()
                    if sub_best_score is not None:
                        new_score = sub_best_score + cost
                        if best_score is None or new_score < best_score:
                            best_score = new_score
                    dest.move(node)
        
        cache[cur_hash] = best_score
        return best_score

print(find_solutions())
