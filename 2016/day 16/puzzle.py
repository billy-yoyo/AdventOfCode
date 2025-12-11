
def gen_data(init, size):
    data = init
    while len(data) < size:
        a, b = data, data
        b = "".join(["0" if c == "1" else "1" for c in reversed(b)])
        data = f"{a}0{b}"
    return data[:size]

def checksum(data):
    while len(data) % 2 == 0:
        data = [
            "1" if data[i] == data[i + 1] else "0" for i in range(0, len(data), 2)
        ]
    return "".join(list(data))

print(checksum(gen_data("10010000000110000", 35651584)))
