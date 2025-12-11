
data = "6,19,0,5,7,13,1"

memory = {}
last_n = 0
for i, n in enumerate([int(x) for x in data.split(",")]):
    memory[last_n] = i - 1
    last_n = n
    #print(f"turn {i+1}: {n}")

i += 1
while i < 30000000:
    if last_n in memory:
        n = i - (memory[last_n] + 1)
    else:
        n = 0
    #print(f"turn {i+1}: ({last_n} ->) {n}")
    memory[last_n] = i - 1
    last_n = n
    i += 1

print(last_n)

