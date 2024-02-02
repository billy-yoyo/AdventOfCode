
with open("input") as f:
    data = f.read().strip().split("\n")

def has_abba(part):
    for i in range(len(part) - 3):
        if part[i] == part[i + 3] and part[i + 1] == part[i + 2] and part[i] != part[i + 1]:
            return True
    return False

def get_aba_pairs(part):
    pairs = set()
    for i in range(len(part) - 2):
        if part[i] == part[i + 2] and part[i] != part[i + 1]:
            pairs |= {part[i:i+2]}
    return pairs 

def get_all_pairs(parts):
    pairs = set()
    for part in parts:
        pairs |= get_aba_pairs(part)
    return pairs

valid = 0
ssl_valid = 0
for line in data:
    parts = line.split("[")
    outside = [parts[0]]
    inside = []
    for part in parts[1:]:
        index = part.index("]")
        outside.append(part[index+1:])
        inside.append(part[:index])

    if any(has_abba(x) for x in outside) and not any(has_abba(x) for x in inside):
        valid += 1
    
    #print(outside, get_all_pairs(outside))

    for pair in get_all_pairs(outside):
        bab = "".join([pair[1], pair[0], pair[1]])
        if any(bab in x for x in inside):
            ssl_valid += 1
            break

print(valid)
print(ssl_valid)    
