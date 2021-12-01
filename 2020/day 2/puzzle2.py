
with open("passwords.txt", "r") as f:
    data = f.readlines()

valid = 0
for line in data:
    policy, password = line.split(":")
    policy_range, char = policy.split(" ")
    lower, upper = [int(n) for n in policy_range.split("-")]

    count = sum(1 if password[pos] == char else 0 for pos in [lower, upper])
    if count == 1:
        valid += 1

print(valid)
