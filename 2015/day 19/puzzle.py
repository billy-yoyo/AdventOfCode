subs = []

with open("data") as f:
    for line in f:
        if "=>" in line:
            left, right = line.split("=>")
            subs.append((left.strip(), right.strip()))
        elif line.strip():
            start = line.strip()

def perform_reduction(s, left, right):
    index = s.find(right)
    while index > -1:
        yield s[:index] + left + s[index+len(right):]
        index = s.find(right, index + 1)

def find_reductions(start):
    todo = [(start, 0)]

    while todo:
        new_todo = []
        for s, swaps in todo:
            if s == "e":
                yield swaps
            else:
                for sub in subs:
                    for reduction in perform_reduction(s, *sub):
                        new_todo.append((reduction, swaps + 1))
        
        todo = new_todo
        

print(next(find_reductions(start)))