
def swap_position(s, x, y):
    x, y = min(x, y), max(x, y)
    if x == y:
        return s
    else:
        return s[:x] + s[y] + s[x+1:y] + s[x] + s[y+1:]

def swap_letter(s, x, y):
    xi, yi = s.index(x), s.index(y)
    return swap_position(s, xi, yi)

def rotate_right(s, x):
    x = x % len(s)
    return s[-x:] + s[:-x]

def rotate_left(s, x):
    x = x % len(s)
    return s[x:] + s[:x]

def rotate_relative(s, x):
    xi = s.index(x)
    return rotate_right(s, xi + 1 + (xi >= 4))

def inverted_rotate_relative(s, x):
    for i in range(len(s)):
        # could i have been the old x?
        old_s = rotate_left(s, i + 1 + (i >= 4))
        if old_s.index(x) == i:
            return old_s
    return s

def reverse(s, x, y):
    x, y = min(x, y), max(x, y)
    return s[:x] + s[x:y+1][::-1] + s[y+1:]

def move(s, x, y):
    if y < x:
        return s[:y] + s[x] + s[y:x] + s[x+1:]
    else:
        return s[:x] + s[x+1:y+1] + s[x] + s[y+1:]

def parse(s, cmd):
    cmd = cmd.strip().split(" ")
    if cmd[0] == "swap" and cmd[1] == "position":
        return swap_position(s, int(cmd[2]), int(cmd[-1]))
    elif cmd[0] == "swap" and cmd[1] == "letter":
        return swap_letter(s, cmd[2], cmd[-1])
    elif cmd[0] == "rotate" and cmd[1] == "left":
        return rotate_left(s, int(cmd[2]))
    elif cmd[0] == "rotate" and cmd[1] == "right":
        return rotate_right(s, int(cmd[2]))
    elif cmd[0] == "rotate" and cmd[1] == "based":
        return rotate_relative(s, cmd[-1])
    elif cmd[0] == "reverse":
        return reverse(s, int(cmd[2]), int(cmd[-1]))
    elif cmd[0] == "move":
        return move(s, int(cmd[2]), int(cmd[-1]))
    else:
        raise Exception(f"Invalid command: {cmd}")

def parse_inverted(s, cmd):
    cmd = cmd.strip().split(" ")
    if cmd[0] == "swap" and cmd[1] == "position":
        return swap_position(s, int(cmd[2]), int(cmd[-1]))
    elif cmd[0] == "swap" and cmd[1] == "letter":
        return swap_letter(s, cmd[2], cmd[-1])
    elif cmd[0] == "rotate" and cmd[1] == "left":
        return rotate_right(s, int(cmd[2]))
    elif cmd[0] == "rotate" and cmd[1] == "right":
        return rotate_left(s, int(cmd[2]))
    elif cmd[0] == "rotate" and cmd[1] == "based":
        return inverted_rotate_relative(s, cmd[-1])
    elif cmd[0] == "reverse":
        return reverse(s, int(cmd[2]), int(cmd[-1]))
    elif cmd[0] == "move":
        return move(s, int(cmd[-1]), int(cmd[2]))
    else:
        raise Exception(f"Invalid command: {cmd}")


with open("input") as f:
    cmds = f.read().strip().split("\n")


password = "fbgdceah"
for line in reversed(cmds):
    password = parse_inverted(password, line)

print(password)

