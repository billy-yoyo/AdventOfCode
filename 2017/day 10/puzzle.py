
def perform_twists(data, inputs, pointer, skip_size):
    size = len(data)
    for input in inputs:
        for i in range(input // 2):
            ai, bi = (pointer + i) % size, (pointer + (input - (i + 1))) % size
            data[ai], data[bi] = data[bi], data[ai]
        pointer += input + skip_size
        skip_size += 1
    return pointer, skip_size

def hexify(x):
    s = hex(x)[2:]
    if len(s) == 1:
        return f"0{s}"
    else:
        return s

def hash_bytes(inputs):
    data = list(range(256))
    inputs += [17, 31, 73, 47, 23]
    pointer, skip_size = 0, 0
    for _ in range(64):
        pointer, skip_size = perform_twists(data, inputs, pointer, skip_size)
    
    chunks = []
    for chunk in range(16):
        chunk_start, chunk_end = chunk * 16, (chunk + 1) * 16
        chunk_value = data[chunk_start]
        for i in range(chunk_start + 1, chunk_end):
            chunk_value ^= data[i]
        chunks.append(chunk_value)
    
    return "".join([hexify(x) for x in chunks])

def hash(string):
    return hash_bytes([ord(c) for c in string])

real = (256, [18,1,0,161,255,137,254,252,14,95,165,33,181,168,2,188])
example = (5, [3, 4, 1, 5])

print(hash("18,1,0,161,255,137,254,252,14,95,165,33,181,168,2,188"))
