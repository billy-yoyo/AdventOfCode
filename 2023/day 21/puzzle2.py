import math

with open("input") as f:
    data = f.read().strip().split("\n")

width = len(data[0])
height = len(data)
initial_start = [(x, y) for y, l in enumerate(data) for x, c in enumerate(l) if c == "S"][0]

def get(x, y):
    c = data[y % height][x % width]
    if c == "S":
        return "."
    else:
        return c

def is_outside(x, y):
    return x < 0 or x >= width or y < 0 or y >= height 


#def is_outside(x, y):
#    return x < 0 or x >= width or y < 0 or y >= height 

MAX_STEPS = 26501365

# our starting row and column is infinitly empty, so we'll always be able to walk
# this then splits our input into a giant grid of "complete" areas, plus a lot of "triangle" areas on the edges of the maximum diamond
# width of this mega-diamond in map-squares is span_width / width
span_width = 1 + (MAX_STEPS * 2)

# we can ignore the central map-square though as we know this reaches the end
# we now know we have (diamond_width - 1) // 2 triangles in each quadrant.
# we enter each triangle from its closest square to the S square, and have (width - 5) // 2 steps remaining

diamond_width = span_width // width
diamond_internal_area = diamond_width * diamond_width

tri_steps_remaining = initial_start[0]

offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def count_internal(start, steps_remaining):
    hit_times = dict()

    stack = [start]
    hit_times[start] = 0

    for i in range(steps_remaining):
        next_stack = []
        for x, y in stack:
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if not is_outside(nx, ny) and  get(nx, ny) == "." and (nx, ny) not in hit_times:
                    hit_times[(nx, ny)] = i + 1
                    next_stack.append((nx, ny))
        stack = next_stack
    
    return sum(1 for k, v in hit_times.items() if v % 2 == steps_remaining % 2)
    
def naive(steps):
    hit_times = dict()

    stack = [initial_start]
    hit_times[initial_start] = 0

    for i in range(steps):
        next_stack = []
        for x, y in stack:
            for ox, oy in offsets:
                nx, ny = x + ox, y + oy
                if get(nx, ny) == "." and (nx, ny) not in hit_times:
                    hit_times[(nx, ny)] = i + 1
                    next_stack.append((nx, ny))
        stack = next_stack

    print(sum(1 for k, v in hit_times.items() if v % 2 == steps % 2))

print(tri_steps_remaining)

mid_left = count_internal((width - 1, initial_start[1]), tri_steps_remaining)
mid_right = count_internal((0, initial_start[1]), tri_steps_remaining)
mid_top = count_internal((initial_start[0], height - 1), tri_steps_remaining)
mid_bot = count_internal((initial_start[0], 0), tri_steps_remaining)

top_left = count_internal((0, 0), tri_steps_remaining)
top_right = count_internal((width - 1, 0), tri_steps_remaining)
bot_left = count_internal((0, height - 1), tri_steps_remaining)
bot_right = count_internal((width - 1, height - 1), tri_steps_remaining)

end_cap_triangles = mid_left + mid_right + mid_top + mid_bot

total_triangles = top_left + top_right + bot_left + bot_right

full_even = count_internal(initial_start, width * 4)
full_odd = count_internal(initial_start, (width * 4) + 1)

print(mid_left)
print(mid_right)
print(mid_top)
print(mid_bot)
print(top_left)
print(top_right)
print(bot_left)
print(bot_right)
print(full_even)
print(full_odd)

f_odd = lambda x: (2 * math.floor((x + 1) / 4)) ** 2
f_even = lambda x: (( 2 * math.floor((x - 1) / 4)) + 1) ** 2

total = 0
total += f_odd(diamond_width - 2) * full_odd
total += f_even(diamond_width - 2) * full_even

#for i in range(0, (diamond_width - 1) // 2):
#    current_height = diamond_width - (i * 2)
#    total += ((current_height - 2) // 2) * (full_even + full_odd)
#    if i % 2 == 0:
#        total += full_odd
#    else:
#        total += full_even

    
# the perimiter should consist of an equal number of each triangles, with the total number of a single triangle being (diamond_width + 1) // 2
number_of_triangles = (diamond_width - 3) // 2

total += top_left * number_of_triangles
total += top_right * number_of_triangles
total += bot_left * number_of_triangles
total += bot_right * number_of_triangles

total += end_cap_triangles

print(total)

"""
offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
hit_times = dict()

stack = [initial_start]
hit_times[initial_start] = 0

# f(5000) = 25 * f(1000) + e
# f(1000) = 4 * f(500) + e
# f(5000) = 100 * f(500) + e
# 
# so f(Ax) = A**2 * f(x) + e
# and f(x) == 1
# so 

total = 0
for i in range(5000):
    if i % 100_000 == 0:
        print(f"done {i}")
    next_stack = []
    for x, y in stack:
        for ox, oy in offsets:
            nx, ny = x + ox, y + oy
            if get(nx, ny) == "." and (nx, ny) not in hit_times:
                hit_times[(nx, ny)] = i + 1
                next_stack.append((nx, ny))
    stack = next_stack

# 1 / 1
# 3 / 2
# 6 / 4
# 9 / 6
#print(hit_times)
    
print(sum(1 for k, v in hit_times.items() if v % 2 == MAX_STEPS % 2))


"""