
age_stack = []

def add_fish(day, amount):
    while len(age_stack) <= day:
        age_stack.append(0)
    age_stack[day] += amount

def process_day():
    birthing = age_stack.pop(0)
    add_fish(6, birthing)
    add_fish(8, birthing)

with open("input") as f:
    input = f.read()

for x in [int(x) for x in input.strip().split(",")]:
    add_fish(x, 1)

for day in range(256):
    process_day()

print(sum(age_stack))