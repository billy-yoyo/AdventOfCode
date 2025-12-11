
r = "abcdPf"

formatters = {
  "addr": lambda a, b, c: f"{r[c]} = {r[a]} + {r[b]}",
  "addi": lambda a, b, c: f"{r[c]} = {r[a]} + {b}",
  "mulr": lambda a, b, c: f"{r[c]} = {r[a]} * {r[b]}",
  "muli": lambda a, b, c: f"{r[c]} = {r[a]} * {b}",
  "banr": lambda a, b, c: f"{r[c]} = {r[a]} & {r[b]}",
  "bani": lambda a, b, c: f"{r[c]} = {r[a]} & {b}",
  "borr": lambda a, b, c: f"{r[c]} = {r[a]} | {r[b]}",
  "bori": lambda a, b, c: f"{r[c]} = {r[a]} | {b}",
  "setr": lambda a, b, c: f"{r[c]} = {r[a]}",
  "seti": lambda a, b, c: f"{r[c]} = {a}",
  "gtir": lambda a, b, c: f"{r[c]} = {a} > {r[b]}",
  "gtri": lambda a, b, c: f"{r[c]} = {r[a]} > {b}",
  "gtrr": lambda a, b, c: f"{r[c]} = {r[a]} > {r[b]}",
  "eqir": lambda a, b, c: f"{r[c]} = {a} == {r[b]}",
  "eqri": lambda a, b, c: f"{r[c]} = {r[a]} == {b}",
  "eqrr": lambda a, b, c: f"{r[c]} = {r[a]} == {r[b]}"
}

output = ["(a, b, c, d, P, f)"]
with open("input") as f:
  for line in f.read().strip().split("\n")[1:]:
    name, a, b, c = line.strip().split(" ")
    output.append(formatters[name](int(a), int(b), int(c)))
  
with open("input_parsed", "w") as f:
  f.write("\n".join(output))
