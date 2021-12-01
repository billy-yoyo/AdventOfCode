
class NodeIter:
    def __init__(self, node):
        self.node = node

    def __next__(self):
        if self.node is None:
            raise StopIteration()

        node = self.node
        self.node = self.node.tail
        return node

class Node:
    def __init__(self, value, tail=None, parent=None):
        self.value = value
        self.tail = tail
        self.parent = parent

    def __str__(self):
        if self.tail:
            return f"{self.value} -> {self.tail}"
        else:
            return str(self.value)

    def copy(self, parent=None):
        node = Node(self.value, parent=parent)

        if self.tail:
            node.tail = self.tail.copy(parent=node)
        
        return node

    def find_tail(self):
        tail = self
        while tail.tail is not None:
            tail = tail.tail
        return tail

    def get(self, i):
        if i == 0:
            return self
        elif self.tail is None:
            return None
        else:
            return self.tail.get(i - 1)

    def __len__(self):
        if self.tail is None:
            return 1
        else:
            return 1 + len(self.tail)

    def __iter__(self):
        return NodeIter(self)

    def __eq__(self, lst):
        return lst is not None and self.value == lst.value and self.tail == lst.tail


def linked_list(lst):
    if not lst:
        return None
    head = Node(lst[0])
    tail = head
    for elt in lst[1:]:
        next_tail = Node(elt, parent=tail)
        tail.tail = next_tail
        tail = next_tail
    return head

subs = {}

def split_molecule(molecule):
    elements = []
    marker = 0
    for i, c in enumerate(molecule):
        if i > 0 and c.lower() != c:
            elements.append(molecule[marker:i])
            marker = i
    elements.append(molecule[marker:])
    return linked_list(elements)

with open("data") as f:
    for line in f:
        if "=>" in line:
            left, right = line.split("=>")
            left, right = left.strip(), split_molecule(right.strip())

            if left not in subs:
                subs[left] = []

            subs[left].append(right)
        elif line.strip():
            target = split_molecule(line.strip())

target_len = len(target)
best_swaps = None

def perform_subs(inp, node=None, index=0, considered=None, swaps=0):
    if index == 0:
        node = inp
    
    if considered is None:
        considered = []

    if best_swaps is not None and swaps >= best_swaps:
        return

    # print(swaps)

    if inp == target:
        yield inp, swaps
    elif node is not None and index < target_len:
        target_node = target.get(index)

        if node.value == target_node.value:
            yield from perform_subs(inp, index=index + 1, node=node.tail, swaps=swaps)
    
        for original in subs.get(node.value, []):
            if original.value not in considered:
                head = original.copy()
                tail = head.find_tail()
                tail.tail = node.tail

                new_inp = inp
                if node.parent is None:
                    new_inp = head
                else:
                    node.parent.tail = head
                
                # new_swaps = swaps + [f"({cur_inp_str}) => {index}/{node.value}/{str(original).replace(' -> ', '')} => ({new_inp})"]
                new_swaps = swaps + 1

                yield from perform_subs(new_inp, index=index, node=head, swaps=new_swaps, considered=considered+[original.value])

                if node.parent is not None:
                    node.parent.tail = node
         
for result, swaps in perform_subs(Node("e")):
    print(f"found result in {swaps} swaps")
    if best_swaps is None or swaps < best_swaps:
        best_swaps = swaps

print(f"smallest chain took {best_swaps} steps")

