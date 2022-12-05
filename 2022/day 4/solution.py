
data = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()

with open("puzzle") as f:
    data = f.read()

ranges = [[[int(x) for x in r.split("-")] for r in line.split(",")] for line in data.split("\n")]

count = 0
for left, right in ranges:
    if left[0] <= right[1] and left[1] >= right[0]:
        count += 1
    
print(count)
