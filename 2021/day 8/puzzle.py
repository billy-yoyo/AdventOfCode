import itertools

with open("input") as f:
    input = f.read()
lines = [[x.strip().split(" ") for x in line.strip().split(" | ")] for line in input.split("\n")]

numbers = [
    [],
    [],
    [(1, "cf")],
    [(7, "acf")],
    [(4, "bcdf")],
    [(2, "acdeg"), (3, "acdfg"), (5, "abdfg")],
    [(0, "abcefg"), (6, "abdefg"), (9, "abcdfg")],
    [(8, "abcdefg")]
]

def generate_valid(nums):
    if len(nums) == 0:
        return [set()]
    valid = []
    for n in nums[0]:
        valid += [set(n) | x for x in generate_valid([x - set(n) for x in nums[1:]])]
    return valid

def decode(line):
    letters = set("abcdefg")
    segs = {"a": set(letters), "b": set(letters), "c": set(letters), "d": set(letters), "e": set(letters), "f": set(letters), "g": set(letters)}
    inp, out = line
    for word in inp:
        possible_numbers = numbers[len(word)]
        possible_letters = set()
        for n, nword in possible_numbers:
            possible_letters |= set(nword)

        for c in word:
            segs[c] &= possible_letters

    was_change = True
    while was_change:
        was_change = False
        for i in range(1, len(letters) - 1):
            for perm in itertools.combinations([l for l, v in segs.items() if len(v) == i], i):
                lets = segs[perm[0]]
                if all(segs[p] == lets for p in perm[1:]):
                    for l in letters:
                        if l not in perm and len(segs[l] & lets) > 0:
                            segs[l] -= lets
                            was_change = True
            
    #print(segs)
    refined_numbers = [[[n, nword, generate_valid([set(x for x, lets in segs.items() if c in lets) for c in nword])] for n, nword in numberset] for numberset in numbers]
    #print(refined_numbers)

    nums = []
    for word in out:
        possible_numbers = refined_numbers[len(word)]
        if len(possible_numbers) == 1:
            nums.append(possible_numbers[0][0])
        else:
            for n, nword, possible in possible_numbers:
                #print(possible)
                if any(all(c in word for c in pword) for pword in possible):
                    nums.append(n)
                    break
    
    return nums

total = 0
for line in lines:
    total += int("".join(str(x) for x in decode(line)))
print(total)