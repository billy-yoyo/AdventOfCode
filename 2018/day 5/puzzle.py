
def explode(string):
    stack = []
    for c in string:
        opposite = c.lower() if c.upper() == c else c.upper()
        if len(stack) and stack[-1] == opposite:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)

def shortest_explosion(string):
    letters = set(string.lower())
    return min(len(explode(string.replace(l, "").replace(l.upper(), ""))) for l in letters) 

with open("input") as f:
    data = f.read().strip()

print(len(explode(data)))
print(shortest_explosion(data))
