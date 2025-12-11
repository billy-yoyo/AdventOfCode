import re
import json


def split_range_left(r, point):
    left, right = r
    if point <= left:
        return [(False, r)]
    elif point >= right:
        return [(True, r)]
    else:
        return [(True, (left, point)), (False, (point, right))]

def split_range_right(r, point):
    left, right = r
    if point < left:
        return [(True, r)]
    elif point >= right - 1:
        return [(False, r)]
    else:
        return [(False, (left, point + 1)), (True, (point + 1, right))]


def parse_instruction(instruction):
    if len(instruction) == 1:
        destination = instruction[0]
        return lambda x: (None, None, destination)
    else:
        condition, destination = instruction
        if "<" in condition:
            word, number = condition.split("<")
            number = int(number)
            runner = lambda x: (word, split_range_left(x[word], number), destination)
        elif ">" in condition:
            word, number = condition.split(">")
            number = int(number)
            runner = lambda x: (word, split_range_right(x[word], number), destination)
        else:
            raise Exception(f"Invalid instruction {instruction}")
        
        return runner
    
def parse_workflow(instructions):
    # returns [(destionation, item)]
    def runner(x):
        final_items = []
        cur_x = x
        for ins in instructions:
            con_word, new_ranges, destination = ins(cur_x)
            if con_word is None:
                final_items.append((destination, cur_x))
                break
            else:
                for valid, r in new_ranges:
                    if r[0] == r[1]:
                        continue
                    
                    new_x = cur_x | { con_word: r }
                    if valid:
                        final_items.append((destination, new_x))
                    else:
                        cur_x = new_x

        return final_items

    return runner

with open("input") as f:
    workflows, items = f.read().strip().split("\n\n")
    workflows = {
        name: parse_workflow([
            parse_instruction(x.split(":")) for x in instructions[:-1].split(",")
        ]) for name, instructions in [w.strip().split("{") for w in workflows.strip().split("\n")]
    }
    items = re.sub(r"([a-zA-Z]+)=", "\"\\1\":", items)
    items = [json.loads(item) for item in items.strip().split("\n")]

def run_workflow(workflows, name, item):
    if name not in workflows:
        raise Exception(f"Workflow {name} doesn't exist")
    
    return workflows[name](item)


def execute_full_workflow(workflows, item):
    valid_items = []

    stack = [("in", item)]
    for destination, next_item in stack:
        if destination == "A":
            valid_items.append(next_item)
            continue

        if destination == "R":
            continue

        for new_destination, new_item in run_workflow(workflows, destination, next_item):
            stack.append((new_destination, new_item))

    return valid_items

total = 0
for valid_item in execute_full_workflow(workflows, { k: (1, 4001) for k in items[0].keys() }):
    prod = 1
    for left, right in valid_item.values():
        prod *= (right - left)
    total += prod
print(total)

#total = 0
#for item in items:
#    if execute_workflow(workflows, "in", item):
#        total += sum(item.values())

#print(total)
