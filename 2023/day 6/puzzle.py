

def race_size(time, distance):
    total = 0
    for i in range(1, time):
        travelled = i * (time - i)
        if travelled > distance:
            total += 1
    return total



def find_lower(time, distance):
    for i in range(1, time):
        travelled = i * (time - i)
        if travelled > distance:
            return i
        
def find_upper(time, distance):
    for i in range(time - 1, 0, -1):
        travelled = i * (time - i)
        if travelled > distance:
            return i


def sum_to_n(n):
    return n * (n + 1)  / 2

def sum_to_n2(n):
    return n * (n + 2) * ((2 * n) + 1) / 6

with open("example") as f:
    lines = [x.split(":")[1].strip() for x in  f.read().strip().split("\n")]
    times, distances = [[int(y) for y in x.split()] for x in lines]
    prod = 1
    for time, distance in zip(times, distances):
        prod *= race_size(time, distance)
    print(prod)

    big_time, big_distance = [int(x.replace(" ", "")) for x in lines]
    lower = find_lower(big_time, big_distance)    
    upper = find_upper(big_time, big_distance)
    print(1 + upper - lower)




