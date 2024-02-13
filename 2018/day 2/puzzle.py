
with open("input") as f:
    words = f.read().strip().split("\n")

with_two = 0
with_three = 0

for word in words:
    has_two = False
    has_three = False
    for c in set(word):
        if word.count(c) == 2:
            has_two = True
        if word.count(c) == 3:
            has_three = True
    with_two += has_two
    with_three += has_three

print(with_two * with_three)

def find_pair():
    for i, word in enumerate(words):
        for j in range(i):
            other_word = words[j]
            errors = 0
            for a, b in zip(word, other_word):
                if a != b:
                    errors += 1
            if errors == 1:
                return word, other_word
            
word, other_word = find_pair()
fixed = []
for a, b in zip(word, other_word):
    if a == b:
        fixed.append(a)
print("".join(fixed))

