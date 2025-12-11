
import re

class Token:
    def __init__(self, name, content, pointer):
        self.name = name
        self.content = content
        self.pointer = pointer

    def __str__(self):
        return self.name

class Tokenizer:
    def __init__(self):
        self.consumers = {}

    def add_consumer(self, name, consumer):
        self.consumers[name] = consumer

    def consume(self, s, pointer):
        best_length = None
        best_name = None
        for name, consumer in self.consumers.items():
            length = consumer(s)
            if best_length is None or length > best_length:
                best_length = length
                best_name = name

        if best_name is not None:
            return Token(best_name, s[:best_length], pointer), s[best_length:]
        else:
            return None, s

    def consume_all(self, s):
        tokens = []
        pointer = (0, 0)
        token, s = self.consume(s, pointer)
        while token is not None and s:
            tokens.append(token)
            lines = token.content.split("\n")
            if len(lines) > 1:
                pointer = (pointer[0] + len(lines) - 1, len(lines[-1]))
            else:
                pointer = (pointer[0], pointer[1] + len(lines[0]))
            token, s = self.consume(s, pointer)

        if token:
            tokens.append(token)

        if s:
            raise ValueError(f"failed to consume rest of string: {s}")

        return tokens

def word_consumer(word):
    return lambda s: len(word) if s.startswith(word) else 0

def wordlist_consumer(words):
    return lambda s: max(len(word) if s.startswith(word) else 0 for word in words)

def regex_consumer(pattern):
    regex = re.compile(pattern)

    def consumer(s):
        match = regex.match(s)
        if match is not None:
            return len(match.group(0))
        else:
            return 0
    
    return consumer

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pointer = 0
    
    def next(self):
        if self.pointer < len(self.tokens):
            token = self.tokens[self.pointer]
            self.pointer += 1
            return token
        return None

tokenizer = Tokenizer()
tokenizer.add_consumer("open", word_consumer("("))
tokenizer.add_consumer("close", word_consumer(")"))
tokenizer.add_consumer("int", regex_consumer(r"^[0-9]+"))
tokenizer.add_consumer("op", wordlist_consumer(["+", "*"]))
tokenizer.add_consumer("whitespace", regex_consumer(r"^\s+"))

def read_value(stream):
    token = stream.next()

    if token is None:
        return None

    if token.name == "int":
        value = int(token.content)
        return value
    elif token.name == "open":
        value = evaluate(stream)
        return value
    else:
        return None

def evaluate(stream):
    values = [read_value(stream)]
    ops = []

    op = stream.next()
    while op is not None and op.name == "op":
        next_value = read_value(stream)
        assert next_value is not None

        ops.append(op.content)
        values.append(next_value)

        op = stream.next()

    mult_values = []
    # collapse additions first
    buffered_value = values[0]
    for i, op in enumerate(ops):
        if op == "*":
            mult_values.append(buffered_value)
            buffered_value = values[i + 1]
        else:
            buffered_value += values[i + 1]
    mult_values.append(buffered_value)

    total = 1
    for value in mult_values:
        total *= value

    return total

def create_stream(s):
    tokens = tokenizer.consume_all(s)
    tokens = [token for token in tokens if token.name != "whitespace"]
    return TokenStream(tokens)


with open("data") as f:
    total = 0
    for line in f:
        if line.strip():
            total += evaluate(create_stream(line.strip()))
print(total)