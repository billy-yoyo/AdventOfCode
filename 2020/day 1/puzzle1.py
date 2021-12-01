

numbers = []
remainders = []
with open("input1.txt") as f:
    for line in f:
        n = int(line.strip())
        numbers.append(n)
        remainders.append(2020 - n)

        for rem in remainders:
            if rem - n in numbers:
                print(f"{2020 - rem} * {n} * {rem - n} = {(2020 - rem) * n * (rem - n)}")
    else:
        print("no pair")

