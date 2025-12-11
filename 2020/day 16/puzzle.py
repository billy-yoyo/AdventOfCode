
rules = []

def read_ticket(line):
    return [int(x) for x in line.strip().split(",")]

def read_rule(line):
    name, value = line.strip().split(":")
    name = name.strip()
    ranges = value.strip().split(" or ")
    ranges = [r.split("-") for r in ranges]
    ranges = [(int(lower), int(upper)) for lower, upper in ranges]

    rules.append((name, ranges))

def value_valid_for_rule(value, rule):
    return any(l <= value <= r for l, r in rule[1])

with open("data") as f:
    raw_rules, raw_my_ticket, raw_other_tickets = f.read().split("\n\n")[:3]

    for rule in raw_rules.split("\n"):
        read_rule(rule)

    my_ticket = read_ticket(raw_my_ticket.split("\n")[1])
    other_tickets = [
        read_ticket(ticket) for ticket in raw_other_tickets.split("\n")[1:]
    ]

possible_fields = {
    rule[0]: list(range(len(my_ticket))) for rule in rules
}


other_tickets.append(my_ticket)
for ticket in other_tickets:
    if any(not any(value_valid_for_rule(value, rule) for rule in rules) for value in ticket):
        continue

    for i, value in enumerate(ticket):
        for rule in rules:
            # filter this index from possible fields for this rule
            if not value_valid_for_rule(value, rule):
                remaining_fields = possible_fields[rule[0]]
                if i in remaining_fields:
                    remaining_fields.remove(i)

def filter_excess_fields(isolated_fields):
    changes = 0
    for field_name, fields in possible_fields.items():
        if len(fields) > 1:
            new_fields = [field for field in fields if field not in isolated_fields]
            if len(new_fields) != len(fields):
                possible_fields[field_name] = new_fields
                if len(new_fields) == 1:
                    isolated_fields.append(new_fields[0])
                changes += 1
    return changes


def filter_possible_fields():
    isolated_fields = []
    for field_name, fields in possible_fields.items():
        if len(fields) == 1:
            isolated_fields.append(fields[0])

    while filter_excess_fields(isolated_fields) > 0:
        pass

filter_possible_fields()
print(possible_fields)

result = 1
for rule_name, fields in possible_fields.items():
    if rule_name.startswith("departure"):
        if len(fields) != 1:
            print(f"possible fields for {rule_name}: {fields}")
            break
        result *= my_ticket[fields[0]]

print(result)