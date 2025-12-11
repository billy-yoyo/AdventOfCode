

def get_index(x, y):
    diagonal = x + y
    prediag = diagonal * (diagonal + 1) // 2
    return prediag + x

def get(n):
    x = 20151125
    for _ in range(n):
        x = (x * 252533) % 33554393
    return x

print(get(get_index(3018, 3009)))

"""
print(f"   | 1   2   3   4   5   6  ")
print(f"---+---+---+---+---+---+---+")
for y in range(6):
    print(f" {y} |", end="")
    for x in range(6):
        i = get_index(x, y)
        istr = str(i) + (" " * (3 - len(str(i))))
        print(istr, end="|")
    print("")
"""