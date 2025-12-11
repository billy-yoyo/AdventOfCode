

data = {}

def read_line(line):
    name, *fields = line.split(":")
    index = int(name.strip().split(" ")[1])
    fields = [field.strip().split(":") for field in ":".join(fields).strip().split(",")]
    fields = {name.strip(): int(value.strip()) for name, value in fields}

    data[index] = fields

with open("data") as f:
    for line in f:
        read_line(line.strip())

item = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
less_than = ["pomeranians", "goldfish"]
greater_than = ["cats", "trees"]

def consider(field, value):
    if field in less_than:
        return value < item[field]
    elif field in greater_than:
        return value > item[field]
    else:
        return value == item[field]

matches = [index for index, fields in data.items() if all(consider(field, value) for field, value in fields.items())]
print(matches)