
def custom_hash(x):
    total = 0
    for c in x:
        total = ((total + ord(c)) * 17) % 256
    return total

with open("input") as f:
    data = f.read().strip().split(",")

print(sum(custom_hash(x) for _ in data))

ls = [[] for x in range(256)]
for x in data:
    if "-" in x:
        label = x[:-1]
        mode = "sub"
    else:
        label, right = x.split("=")
        focal = int(right)
        mode = "add"
    
    label_hash = custom_hash(label)
    box = ls[label_hash]
    if mode == "sub" and any(x[0] == label for x in box):
        ls[label_hash] = [x for x in box if x[0] != label]
    elif mode == "add":
        if any(x[0] == label for x in box):
            ls[label_hash] = [(label, focal) if x[0] == label else x for x in box]
        else:
            ls[label_hash] += [(label, focal)]

total = 0
for i, box in enumerate(ls):
    for j, (lens, focal) in enumerate(box):
        total += (i + 1) * (j + 1) * focal
    
print(total)
