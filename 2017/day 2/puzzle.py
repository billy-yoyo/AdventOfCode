
with open("input") as f:
    data = f.read().strip().split("\n")

total = 0
result = 0
for line in data:
    nums = [int(x.strip()) for x in line.split() if x.strip()]
    total += max(nums) - min(nums)
    for i, n in enumerate(nums):
        for j in range(i):
            m = nums[j]
            if max(n, m) % min(n, m) == 0:
                result += max(n, m) // min(n, m)
print(total)
print(result)
