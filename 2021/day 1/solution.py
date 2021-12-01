
with open("input") as f:
    data = [int(x.strip()) for x in f.readlines() if x.strip()]
    
last = [data[0] + data[1] + data[2], data[1] + data[2], data[2]]
last_window = 0
n = 0
for cur in data[3:]:
    window = last[0]
    last[0] = last[1] + cur
    last[1] = last[2] + cur
    last[2] = cur

    if window > last_window:
        n += 1
    last_window = window

print(n)
