from collections import defaultdict

with open("input") as f:
    data = f.read().strip().split("\n")

def letter_counts(word):
    counts = defaultdict(int)
    for c in word:
        counts[c] += 1
    return counts

def is_anagram(a, b):
    a_counts = letter_counts(a)
    b_counts = letter_counts(b)
    for letter, count in a_counts.items():
        if b_counts[letter] != count:
            return False
    for letter, count in b_counts.items():
        if a_counts[letter] != count:
            return False
    return True

def valid(words):
    for i, word in enumerate(words):
        for j in range(i):
            if is_anagram(word, words[j]):
                return False
    return True


total = sum(valid(line.split(" ")) for line in data)
print(total)
