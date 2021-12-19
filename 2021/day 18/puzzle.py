import math
import json

class Node:
    @staticmethod
    def from_pair(parent, parent_side, pair):
        left, right = pair
        node = Node(parent, parent_side, None, None)
        if isinstance(left, list) or isinstance(left, tuple):
            node.left = Node.from_pair(node, "left", left)
        else:
            node.left = left
        if isinstance(right, list) or isinstance(right, tuple):
            node.right = Node.from_pair(node, "right", right)
        else:
            node.right = right
        return node

    def __init__(self, parent, parent_side, left, right):
        self.parent = parent
        self.side = parent_side
        self.left = left
        self.right = right
        self.depth = 0 if parent is None else parent.depth + 1

    def find_right_most(self):
        if isinstance(self.right, Node):
            return self.right.find_right_most()
        return self
    
    def find_left_most(self):
        if isinstance(self.left, Node):
            return self.left.find_left_most()
        return self

    def add_to_left(self, value):
        if self.parent is None:
            return
        parent, current = self.parent, self
        while parent is not None and current.side == "left":
            parent, current = parent.parent, current.parent
        if parent is not None:
            if isinstance(parent.left, int):
                parent.left += value
            else:
                parent.left.find_right_most().right += value
    
    def add_to_right(self, value):
        if self.parent is None:
            return
        parent, current = self.parent, self
        while parent is not None and current.side == "right":
            parent, current = parent.parent, current.parent
        if parent is not None:
            if isinstance(parent.right, int):
                parent.right += value
            else:
                parent.right.find_left_most().left += value

    def explode(self):
        if self.depth >= 4:
            self.add_to_left(self.left)
            self.add_to_right(self.right)
            setattr(self.parent, self.side, 0)
        else:
            if isinstance(self.left, Node):
                self.left.explode()
            if isinstance(self.right, Node):
                self.right.explode()

    def split(self):
        if isinstance(self.left, int) and self.left >= 10:
            lower, upper = math.floor(self.left / 2), math.ceil(self.left / 2)
            self.left = Node(self, "left", lower, upper)
            return True
        elif isinstance(self.left, Node):
            if self.left.split():
                return True
        
        if isinstance(self.right, int) and self.right >= 10:
            lower, upper = math.floor(self.right / 2), math.ceil(self.right / 2)
            self.right = Node(self, "right", lower, upper)
            return True
        elif isinstance(self.right, Node):
            if self.right.split():
                return True
        return False

    def add(self):
        self.explode()
        while self.split():
            self.explode()

    def magnitude(self):
        mag = 0
        if isinstance(self.left, int):
            mag += 3 * self.left
        else:
            mag += 3 * self.left.magnitude()
        if isinstance(self.right, int):
            mag += 2 * self.right
        else:
            mag += 2 * self.right.magnitude()
        return mag
    
    def to_list(self):
        return [
            self.left if isinstance(self.left, int) else self.left.to_list(),
            self.right if isinstance(self.right, int) else self.right.to_list()
        ]

    def __str__(self):
        return f"({self.left},{self.right})"

with open("input") as f:
    homework = [json.loads(line) for line in f]

biggest_mag = 0
for i, line_1 in enumerate(homework):
    for j, line_2 in enumerate(homework):
        if i == j:
            continue
        node = Node.from_pair(None, None, [line_1, line_2])
        node.add()
        mag = node.magnitude()
        if mag > biggest_mag:
            biggest_mag = mag
print(biggest_mag)
"""
cur = Node.from_pair(None, None, homework[:2])
cur.add()

for line in homework[2:]:
    root = Node.from_pair(None, None, [cur.to_list(), line])
    cur.parent = root
    cur.side = "left"
    root.add()

    cur = root
print(cur.magnitude())
"""