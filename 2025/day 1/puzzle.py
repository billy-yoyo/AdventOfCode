
offsets = []
with open("data") as f:
  for line in f:
    if line.strip():
      letter, n = line.strip()[0], line.strip()[1:]
      offsets.append(int(n) if letter == "R" else -int(n))

count = 0
dial = 50
for offset in offsets:
  new_dial = dial + offset
  if new_dial == 0 or new_dial == 100:
    count += 1
  elif new_dial < 0:
    cycles = abs(new_dial) // 100
    if dial != 0:
      cycles += 1
    count += cycles
  elif new_dial > 100:
    cycles = new_dial // 100
    count += cycles
  
  dial = new_dial % 100

print(count)