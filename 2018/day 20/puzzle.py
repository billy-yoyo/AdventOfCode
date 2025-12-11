from collections import deque, defaultdict


letters = "ESWN"
def consume_word_pattern(s):
    #print(f"consuming words from {s}")
    pointer = 0
    while pointer < len(s) and  s[pointer] in letters:
        pointer += 1
    return s[:pointer], s[pointer:]

def consume_bracket(s):
    #print(f"consuming bracket from {s}")
    patterns = []
    s = s[1:]
    while s:
        pattern, s = consume_pattern(s)
        patterns.append(pattern)
        if s[0] != "|":
            break
        s = s[1:]
    if not s or s[0] != ")":
        raise SyntaxError()
    return patterns, s[1:]
        
def consume_pattern(s):
    #print(f"consuming pattern from {s}")
    pattern = []
    while s and (s[0] in letters or s[0] == "("):
        if s[0] == "(":
            subpattern, s = consume_bracket(s)
        else:
            subpattern, s = consume_word_pattern(s)
        pattern.append(subpattern)
    return pattern, s

directions = {
    "E": (1, 0),
    "W": (-1, 0),
    "N": (0, -1),
    "S": (0, 1)
}

def build_graph(pattern):
    graph = defaultdict(set)
    stack = deque([((0, 0), pattern)])
    while stack:
        (x, y), pattern = stack.popleft()
        for sub_pattern in pattern:
            # word pattern
            if isinstance(sub_pattern, str):
                for letter in sub_pattern:
                    ox, oy = directions[letter]
                    nx, ny = x + ox, y + oy
                    graph[(x, y)].add((nx, ny))
                    graph[(nx, ny)].add((x, y))
                    x, y = nx, ny
            else:
                for or_pattern in sub_pattern:
                    stack.append(((x, y), or_pattern))
    return graph

def longest_shortest_path_from(graph, start):
    visited = set()
    stack = deque([(start, 0)])
    max_dist = 0
    count = 0
    while stack:
        pos, dist = stack.popleft()
        if dist >= 1000:
            count += 1
        max_dist = max(dist, max_dist)
        for npos in graph[pos]:
            if npos in visited:
                continue
            visited.add(npos)
            stack.append((npos, dist + 1))
    return max_dist, count


with open("input") as f:
    pattern_string = f.read().strip()[1:-1]

pattern, _ = consume_pattern(pattern_string)
graph = build_graph(pattern)
print(longest_shortest_path_from(graph, (0, 0)))


