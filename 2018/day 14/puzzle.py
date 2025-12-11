

def digits(n):
    digits = [n % 10]
    while n >= 10:
        n //= 10
        digits.insert(0, n % 10)
    return digits

def gen(steps):
    data = [3, 7]
    pointers = [0, 1]
    while len(data) < steps + 10:
        n = sum(data[p] for p in pointers)
        data += digits(n)
        for i, p in enumerate(pointers):
            pointers[i] = (p + data[p] + 1) % len(data)
    return "".join(str(x) for x in data)

def part1(steps):
    data = [3, 7]
    pointers = [0, 1]
    while len(data) < steps + 10:
        n = sum(data[p] for p in pointers)
        data += digits(n)
        for i, p in enumerate(pointers):
            pointers[i] = (p + data[p] + 1) % len(data)
    return "".join(str(x) for x in data[steps:steps+10])

def part2(search):
    search_digits = digits(search)

    data = [3, 7]
    pointers = [0, 1]
    while True:
        n = sum(data[p] for p in pointers)
        n_digits = digits(n)
        data += n_digits
        for i in range(len(n_digits)):
            if data[(len(data) - (len(search_digits) + i)):(len(data) - i)] == search_digits:
                return len(data) - (len(search_digits) + i)
        for i, p in enumerate(pointers):
            pointers[i] = (p + data[p] + 1) % len(data)
