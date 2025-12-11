
width = 50
height = 6

screen = [
    ["."] * width for _ in range(height)
]



def rect(cmd):
    a, b = [int(x) for x in cmd.split(" ")[-1].split("x")]
    for x in range(a):
        for y in range(b):
            screen[y][x] = "#"

def rotate(cmd):
    cmd = cmd.split(" ")
    x = int(cmd[2].split("=")[1])
    amount = int(cmd[4])

    if cmd[1] == "row":
        screen[x] = [screen[x][(i - amount) % width] for i in range(width)]
    elif cmd[1] == "column":
        new_column = [
            screen[(i - amount) % height][x] for i in range(height)
        ]
        for i in range(height):
            screen[i][x] = new_column[i]
    else:
        raise Exception(f"invalid command {cmd}")

def parse(cmd):
    if cmd.startswith("rect"):
        rect(cmd)
    elif cmd.startswith("rotate"):
        rotate(cmd)
    else:
        raise Exception(f"invalid command {cmd}")
    
def print_screen():
    print("\n".join("".join(line) for line in screen))

#print_screen()
#print("\n")

with open("input") as f:
    for line in f.read().strip().split("\n"):
        parse(line)
        #print_screen()
        #print("\n")

print_screen()

print(sum(sum(1 for x in line if x == "#") for line in screen)) 

