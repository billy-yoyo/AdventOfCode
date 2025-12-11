from collections import defaultdict

values = defaultdict(list)
targets = {}
outputs = defaultdict(list)

def give_value(bot_id, value):
    values[bot_id].append(value)
    if len(values[bot_id]) == 2:
        low = min(values[bot_id])
        high = max(values[bot_id])

        if low == 17 and high == 61:
            print(bot_id)

        low_type, low_target, high_type, high_target = targets[bot_id]
        if low_type == "bot":
            give_value(low_target, low)
        else:
            outputs[low_target].append(low)
        
        if high_type == "bot":
            give_value(high_target, high)
        else:
            outputs[high_target].append(high)

with open("input") as f:
    lines = f.read().strip().split("\n")
    for line in lines:
        line = line.split(" ")
        if line[0] == "bot":
            targets[int(line[1])] = (
                line[5],
                int(line[6]),
                line[-2],
                int(line[-1])
            )

    for line in lines:
        line = line.split(" ")
        if line[0] == "value":
            give_value(int(line[-1]), int(line[1]))
            
print(outputs[0][0] * outputs[1][0] * outputs[2][0])


#print(values)
#print(targets)
#print(outputs)
#
