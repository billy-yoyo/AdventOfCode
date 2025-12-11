

mem = {}
mask = []

def read_mask(m):
    mask = []
    value = 2 ** 35
    for c in m:
        if c == "X":
            mask.append((c, value))
        elif c == "1":
            mask.append((c, value))
        
        value >>= 1
    return mask

def assign_floating_mem(address, x, mask, i):
    while i < len(mask) and mask[i][0] != "X":
        i += 1
    
    if i < len(mask):
        value = mask[i][1]
        assign_floating_mem(address | value, x, mask, i + 1)
        assign_floating_mem(address & ~value, x, mask, i + 1)
    else:
        mem[address] = x

def assign_mem(address, x, mask):
    # first mask 1s
    for mode, value in mask:
        if mode == "1":
            address |= value

    assign_floating_mem(address, x, mask, 0)
    

def read_ins(line):
    name, value = line.strip().split("=")
    name, value = name.strip(), value.strip()
    
    if name == "mask":
        return read_mask(value)
    else:
        address, value = int(name[4:-1]), int(value)
        assign_mem(address, value, mask)
        return mask

with open("data") as f:
    for line in f:
        mask = read_ins(line)

print(mem)
print(sum(x for x in mem.values()))