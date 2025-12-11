
with open("testinput") as f:
    input = f.read()

#top_left = [20, -10]
#bot_right = [30, -5]
top_left = [29, -248]
bot_right = [73, -194]

def collides_with_y(y):
    miny, maxy = top_left[1], bot_right[1]
    pos = 0
    while pos > maxy:
        #print(f"pos is {pos}, y is {y}")
        pos += y
        y -= 1
    #print(f"checking {miny} <= {pos} <= {maxy}")
    return miny <= pos <= maxy

def collides_with_x(x):
    minx, maxx = top_left[0], bot_right[0]
    pos = 0
    while pos < minx and abs(x) > 0:
        pos += x
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
    return minx <= pos <= maxx

def collides(x, y):
    minx, miny = top_left
    maxx, maxy = bot_right
    px, py = 0, 0
    while px < maxx and py > miny:
        #print(f"pos = ({px}, {py}); vel = ({x}, {y})")
        px += x
        py += y
        y -= 1
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        
        if minx <= px <= maxx and miny <= py <= maxy:
            #print(f"found hit at {px}, {py}")
            return True
    #print(f"overshot at {px}, {py}")
    return False

def find_y():
    y = 1
    while not collides_with_y(y):
        y += 1
    while collides_with_y(y):
        yield y
        y += 1
    #print(f"y of {y} doesnt collide")

def find_x():
    x = 1
    while not collides_with_x(x):
        x += 1
    while collides_with_x(x):
        yield x
        x += 1

def find_highest(y):
    miny, maxy = top_left[1], bot_right[1]
    pos = 0
    while y > 0:
        pos += y
        y -= 1
    return pos
"""
bx, by = 0, 0
for y in find_y():
    for x in find_x():
        if True or collides(x, y):
            print(f"{x}, {y} is valid")
            if y > by:
                bx, by = x, y

print(bx, by)
print(find_highest(by))
"""

"""
hy = y * (y + 1) / 2
hymax = hy - miny
hymin = hy - maxy

hymin <= z * (z + 1) / 2 <= hymax

2 * hymin <= z*z + z <= 2 * hymax


"""
min_y = -248
max_y = 246

min_x = 0
max_x = 73

xs = [x for x in range(min_x, max_x + 1) if collides_with_x(x)]
ys = [y for y in range(min_y, 10000) if collides_with_y(y)]

print(xs)
print(ys)

count = 0
for x in xs:
    for y in ys:
        if collides(x, y):
            count += 1
print(count)


#y = 70"""
#print(collides_with_y(y))#
#print(find_highest(y))

#highest = max([find_highest(y) for y in find_y()])
#print(highest)

