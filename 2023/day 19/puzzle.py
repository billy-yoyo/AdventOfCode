import re
import json

{"x":787,"m":2655,"a":1222,"s":2876}
{"x":1679,"m":44,"a":2067,"s":496}
{"x":2036,"m":264,"a":79,"s":2244}
{"x":2461,"m":1339,"a":466,"s":291}
{"x":2127,"m":1623,"a":2188,"s":1013}

def parse_instruction(instruction):
    if len(instruction) == 1:
        destination = instruction[0]
        return lambda x: destination
    else:
        condition, destination = instruction
        if "<" in condition:
            word, number = condition.split("<")
            number = int(number)
            runner = lambda x: x[word] < number
        elif ">" in condition:
            word, number = condition.split(">")
            number = int(number)
            runner = lambda x: x[word] > number
        else:
            raise Exception(f"Invalid instruction {instruction}")
        
        return lambda x: destination if runner(x) else None
    
def parse_workflow(instructions):
    def runner(x):
        for ins in instructions:
            dest = ins(x)
            if dest is not None:
                return dest
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

def execute_workflow(workflows, name, item):
    if name not in workflows:
        raise Exception(f"Workflow {name} doesn't exist")
    
    next_destination = name
    while next_destination not in "AR":
        if next_destination not in workflows:
            raise Exception(f"Workflow {next_destination} doesn't exist")

        next_destination = workflows[next_destination](item)
    
    return next_destination == "A"

total = 0
for item in items:
    if execute_workflow(workflows, "in", item):
        total += sum(item.values())

print(total)
