from functools import reduce
x=reduce(lambda x,y:[i+j*x[1]for i,j in zip(y,{"f":[0,1,y[0]],"d":[1,0,0],"u":[-1,0,0]}[x[0]])],[(x[0],int(x.split(" ")[1]))for x in open("input").readlines()],[0,0,0])
print(x[1]*x[2])

"""
with open("input") as f:
    data = f.read()

cmds = [x.strip().split(" ") for x in data.split("\n") if x.strip()]
cmds = [(x, int(y)) for x, y in cmds]

aim = 0
x, y = 0, 0

for cmd, amt in cmds:
    if cmd == "forward":
        x += amt
        y += amt * aim
    elif cmd == "down":
        aim += amt
    elif cmd == "up":
        aim -= amt
    else:
        print(f"ignoring cmd {cmd}")

print(x * y)
"""