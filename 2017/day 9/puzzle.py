
def consume_garbage(s, start):
    i = start + 1
    escaped = False
    total_escaped = 0
    while i < len(s):
        if s[i] == ">" and not escaped:
            return i, total_escaped
        elif s[i] == "!" and not escaped:
            escaped = True
        elif escaped:
            total_escaped += 2
            escaped = False
        i += 1
    return len(s), total_escaped

def parse_groups(s):
    total = 0
    garbage_total = 0
    level = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == "{":
            level += 1
        elif c == "}":
            total += level
            level -= 1
        elif c == "<":
            next_i, total_escaped = consume_garbage(s, i)
            garbage_total += next_i - (i + 1 + total_escaped)
            i = next_i
        i += 1
    return total, garbage_total

def test_garbage(s):
    print(s[consume_garbage(s, 0)+1:])

with open("input") as f:
    data = f.read().strip()

#data = "<{o\"i!a,<{i<a>"

print(parse_groups(data))
