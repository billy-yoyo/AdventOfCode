
with open("input") as f:
    input = f.read()

def read_line(line):
    open_brackets = "<([{"
    close_brackets = ">)]}"
    stack = []
    for c in line:
        if c in open_brackets:
            stack.append(c)
        elif c in close_brackets:
            last = stack.pop()
            if open_brackets.index(last) != close_brackets.index(c):
                return 0

    score = 0
    if stack:
        for c in reversed(stack):
            score = (score * 5) + scores[c]
    return score

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

line_scores = sorted([read_line(line) for line in input.split("\n")])
line_scores = [x for x in line_scores if x > 0]

print(line_scores[len(line_scores) // 2])