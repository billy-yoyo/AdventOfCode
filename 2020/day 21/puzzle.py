from collections import defaultdict

all_allergens = set()
all_ingreds = set()
all_foods = []
ingred_counts = defaultdict(int)

def parse_food(line):
    ingreds, allergens = line.strip().split("(")
    ingreds = ingreds.strip().split(" ")
    allergens = [x.strip() for x in allergens[9:-1].split(",")]

    for allergen in allergens:
        all_allergens.add(allergen)
    
    for ingred in ingreds:
        ingred_counts[ingred] += 1
        all_ingreds.add(ingred)

    all_foods.append((set(ingreds), set(allergens)))


def calculate_allergens():
    allergen_candidates = {allergen: set(all_ingreds) for allergen in all_allergens}

    for ingreds, allergens in all_foods:
        for allergen in allergens:
            allergen_candidates[allergen] &= ingreds

    decided = set()
    for candidates in allergen_candidates.values():
        if len(candidates) == 1:
            decided |= candidates
    
    while len(decided) < len(all_allergens):
        for allergen, candidates in allergen_candidates.items():
            if len(candidates) > 1:
                new_candidates = candidates - decided
                allergen_candidates[allergen] = new_candidates
                if len(new_candidates) == 1:
                    decided |= new_candidates

    return allergen_candidates

with open("data") as f:
    for line in f.read().split("\n"):
        if line.strip():
            parse_food(line)

allergen_candidates = calculate_allergens()
pairs = {(allergen, next(iter(ingreds))) for allergen, ingreds in allergen_candidates.items()}
pairs = sorted(pairs, key=lambda pair: pair[0])
print(",".join(pair[1] for pair in pairs))
    
def not_allergen(ingred):
    return all(ingred not in candidates for candidates in allergen_candidates.values())

print(allergen_candidates)

total = 0
for ingred in all_ingreds:
    if not_allergen(ingred):
        total += ingred_counts[ingred]

print(total)