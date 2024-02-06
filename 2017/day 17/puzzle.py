
def index_for(n, total, period):
    if n == 0:
        return 0
    xn = 0
    index = -1
    neighbour = None
    for i in range(1, total):
        xn = ((xn + period) % max(i,1)) + 1
        if i == n:
            index = xn
        elif i > n and xn <= index:
            index += 1
    return index, neighbour


def create_list(total, period):
    data = [None] * total
    data[0] = 0
    data[1] = 1
    xn = 1
    for i in range(2, total):
        xn = ((xn + period) % i) + 1
        #print(f"{i}={xn}")
        data[i] = xn
        for j in range(i):
            if data[j] >= xn:
                data[j] += 1
    return [data.index(x) for x in range(i)]

def leftmost(total, period):
    value = 1
    xn = 1
    for i in range(2, total):
        xn = ((xn + period) % i) + 1
        if xn == 1:
            value = i
    return value

lst = create_list(2018, 335)
index = lst.index(2017)
print(index, lst[index + 1])

print(leftmost(50000000, 335))

