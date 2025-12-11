
with open("input") as f:
    input = f.read()

small_grid = [[int(x) for x in line.strip()] for line in input.strip().split("\n")]
small_width, small_height = len(small_grid[0]), len(small_grid)
width, height = small_width * 5, small_height * 5
grid = [[0] * width for i in range(height)]

def clamp(x):
    while x > 9:
        x -= 9
    return x

for y in range(height):
    oy = y % small_height
    gy = y // small_height
    for x in range(width):
        ox = x % small_width
        gx = x // small_width
        
        value = clamp(small_grid[oy][ox] + gx + gy)
        grid[y][x] = value


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def insert(list, x, key):
    for i, y in enumerate(list):
        if key(y) < key(x):
            break
    list.insert(0, x)


def find_path(start, end):
    min_scores = {}
    stack = [([tuple(start)],0)]
    while stack:
        path, score = stack.pop(0)
        last = path[-1]
        for dir in dirs:
            x, y = last[0] + dir[0], last[1] + dir[1]
            if 0 <= x < width and 0 <= y < height and (x, y) not in path:
                new_path = path + [(x, y)]
                new_score = score + grid[y][x]
                if x == end[0] and y == end[1]:
                    return (new_path, new_score)
                elif (x, y) not in min_scores or new_score < min_scores[(x, y)]:
                    min_scores[(x, y)] = new_score
                    stack.append((new_path, new_score))
        stack = sorted(stack, key=lambda x: x[1], reverse=False)
    return None, 0

path, score = find_path((0, 0), (width - 1, height - 1))
print(path)
print(score)
