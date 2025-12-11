
digit_map = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def first_digit(s):
    for i in range(len(s)):
        for x, v in digit_map.items():
            if s[i:].startswith(x):
                return 10 * v
    return 0

def last_digit(s):
    for i in reversed(range(len(s))):
        for x, v in digit_map.items():
            if s[:(i+1)].endswith(x):
                return v
    return 0

total = 0
with open("input") as f:
    for line in f:
        total += int(first_digit(line) + last_digit(line))

print(total)