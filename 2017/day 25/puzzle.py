from collections import defaultdict



with open("input") as f:
    sections = f.read().strip().split("\n\n")

header = sections[0].strip().split("\n")
initial_state = header[0].strip().split(" ")[-1][:-1]
checksum_after = int(header[1].strip().split(" ")[-2])

state_machines = {}
for section in sections[1:]:
    lines = section.strip().split("\n")
    state = lines[0].strip().split(" ")[-1][:-1]
    cases = {}
    
    lines = lines[1:]
    for subsection in range(((len(lines) - 1) // 4) + 1):
        i = subsection * 4
        cur_value = int(lines[i].strip().split(" ")[-1][:-1])
        write_value = int(lines[i + 1].strip().split(" ")[-1][:-1])
        move_direction = lines[i + 2].strip().split(" ")[-1][:-1]
        next_state = lines[i + 3].strip().split(" ")[-1][:-1]
        cases[cur_value] = (write_value, -1 if move_direction == "left" else 1, next_state)
    state_machines[state] = cases

tape = defaultdict(int)
cursor = 0
state = "A"

for _ in range(checksum_after):
    write, move, next_state = state_machines[state][tape[cursor]]
    tape[cursor] = write
    cursor += move
    state = next_state

print(sum(tape.values()))
