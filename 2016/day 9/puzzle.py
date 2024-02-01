
def parse_length(line):
    start = 0
    inside = False
    total = 0
    #uncompressed = []
    size, repeats = None, None
    for i, c in enumerate(line + "("):
        if inside and c == ")":
            size, repeats = [int(x) for x in line[start:i].split("x")]
            start = i + 1
            inside = False
            size -= 1
        elif not inside and size is not None and size > 0:
            size -= 1
        elif not inside and size is not None and size == 0:
            part = line[start:i+1]
            part_size = parse_length(part)
            total += part_size * repeats
            #uncompressed.append(part * repeats)
            size, repeats = None, None
            start = i + 1
        elif not inside and c == "(":
            part = line[start:i]
            #uncompressed.append(part)
            total += len(part)
            start = i + 1
            inside = True
    #print("".join(uncompressed))
    return total



with open("input") as f:
    for line in f.read().strip().split("\n"):
        length = parse_length(line)
        print(length)
    
    

