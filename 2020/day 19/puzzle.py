
rules = {}

class Stream:
    def __init__(self, s, pointer=0):
        self.s = s
        self.pointer = pointer

    def next(self):
        if self.pointer >= len(self.s):
            return None
        c = self.s[self.pointer]
        self.pointer += 1
        return c

    def finished(self):
        return self.pointer >= len(self.s)

    def branch(self):
        return Stream(self.s, self.pointer)

    def merge(self, branch):
        self.pointer = branch.pointer

def read_line(line):
    index, content = [x.strip() for x in line.split(":")]
    index = int(index)
    content = [x.strip() for x in content.split("|")]
    content = [
        x[1:-1] if x[0] == '"' else [int(y.strip()) for y in x.split(" ")] for x in content
    ]

    rules[index] = content

def parse_single_rule(stream, rule):
    if isinstance(rule, list) or isinstance(rule, tuple):
        branches = [stream]

        for subrule in rule:
            new_branchs = []
            for branch in branches:
                new_branchs += [b for b in parse_rule(branch, rules[subrule])]
            branches = new_branchs

        for branch in branches:
            yield branch
    else:    
        if stream.next() == rule:
            yield stream

def parse_rule(stream, rules):
    for rule in rules:
        branch = stream.branch()
        yield from parse_single_rule(branch, rule)

def match_string(string):
    stream = Stream(string)
    return any(branch.finished() for branch in parse_rule(stream, rules[0]))

with open("data2") as f:
    rule_strings, strings = f.read().split("\n\n")
    for line in rule_strings.split("\n"):
        if line.strip():
            read_line(line.strip())

    total = 0
    for string in strings.split("\n"):
        if string.strip():
            if match_string(string):
                total += 1
                print(f"string {string} matches rule 0")
            else:
                print(f"string {string} doesn't match rule 0")
    print(total)