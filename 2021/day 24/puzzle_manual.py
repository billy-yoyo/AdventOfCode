
with open("input") as f:
    parts = f.read().strip().split("inp w")

stack = []

for i, part in enumerate(parts[1:]):
    part = part.strip().split("\n")
    check = int(part[4].strip().split(" ")[-1])
    offset = int(part[-3].strip().split(" ")[-1])

    #print(f"{check}, {offset}")

    if check <= 0:
        popped_index, popped_offset = stack.pop()
        total_offset = check + popped_offset
        print(f"input[{i}] == input[{popped_index}] {'+' if total_offset >= 0 else '-' } {abs(total_offset)}")
    else:
        stack.append((i, offset))
        #print(f"PUSH input[{i}] + {offset}")

print(stack)

a = 1

#  0: 1
#  1: 2
#  2: 9
#  3: 3
#  4: 4
#  5: 9
#  6: 9
#  7: 8
#  8: 9
#  9: 4
# 10: 9
# 11: 1
# 12: 9
# 13: 9

# smallest
12934998949199

