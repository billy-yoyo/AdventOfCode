from hashlib import md5

key = "cuanljph"
#key = "abc"

def super_hash(s):
    data = s
    for _ in range(2017):
        data = md5(data.encode("utf-8")).hexdigest()
    return data

index = 0
keys = []
potentials = []
while len(keys) < 64:
    hash = super_hash(f"{key}{index}")
    
    new_potentials = []
    for lookup, before in potentials:
        if index <= before and lookup in hash:
            #print(f"found {lookup} (to be found before {before}) at index {index} in hash {hash}")
            keys.append(before - 1000)
            if len(keys) == 64:
                break
        elif index <= before:
            new_potentials.append((lookup, before))
    for i, c in enumerate(hash[:-2]):
        if hash[i + 1] == c and hash[i + 2] == c:
           #print(f"looking for {c} because of {hash}")
            new_potentials.append((c * 5, index + 1000))
            break
    potentials = new_potentials
    index += 1

print(sorted(keys)[-1])
