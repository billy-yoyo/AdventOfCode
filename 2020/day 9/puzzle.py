


def is_valid(stack, n):
    search = {}
    for x in stack:
        if x in search:
            return True
        search[n - x] = True
        search[x] = True
    return False

target = 85848519
with open("data") as f:
    stack = []
    stack_sum = 0
    for line in f.read().split():
        if line:
            n = int(line)

            stack.append(n)
            stack_sum += n

            while stack and stack_sum > target:
                stack_sum -= stack.pop(0)

            if len(stack) > 1 and stack_sum == target:
                print(stack)
                print(stack_sum)
                print(f"weakness: {min(stack) + max(stack)}")
                break

