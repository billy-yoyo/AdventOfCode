

class Node:
    def __init__(self, value, parent=None, child=None):
        self.value = value
        self.parent = parent
        self.child = child

    def find(self, value, stopat=None):
        if self.value == value:
            return self

        node = self.child
        while node.value != value and node != self:
            node = node.child
        if node.value == value:
            return node
        return None

    def splice(self, length):
        head = self

        tail = self
        for _ in range(length - 1):
            tail = tail.child
        
        head.parent.child = tail.child
        tail.child.parent = head.parent

        head.parent = None
        tail.child = None

        return head, tail

    def insert_after(self, head, tail):
        child = self.child
        
        self.child = head
        head.parent = self

        tail.child = child
        child.parent = tail

    def __str__(self):
        values = [self.value]
        node = self.child
        while node is not None and node != self:
            values.append(node.value)
            node = node.child
        return "".join(str(x) for x in values)

    def __eq__(self, node):
        return self.value == node.value

node_map = {}

starting_cups = [int(x) for x in "186524973"]
value = max(starting_cups) + 1
while len(starting_cups) < 1000000:
    starting_cups.append(value)
    value += 1

max_value = max(starting_cups)

head_cup, tail_cup = None, None
for cup in starting_cups:
    new_cup = Node(cup, parent=tail_cup)
    node_map[cup] = new_cup
    if tail_cup is not None:
        tail_cup.child = new_cup
    
    if head_cup is None:
        head_cup = new_cup
    tail_cup = new_cup

tail_cup.child = head_cup
head_cup.parent = tail_cup

def decr(value):
    value = value - 1
    if value < 1:
        return max_value 
    return value

def play_move(head):
    picked_up = head.child.splice(3)

    dest, value = None, decr(head.value)
    while dest is None:
        dest = node_map[value]
        if dest == picked_up[0] or dest == picked_up[0].child or dest == picked_up[1]:
            dest = None
        value = decr(value)

    dest.insert_after(*picked_up)
    return head.child

cup = head_cup
for i in range(10000000):
    cup = play_move(cup)

cup_1 = node_map[1]
print(cup_1.child.value * cup_1.child.child.value)
#print(str(cup_1)[1:])