
with open("data") as f:
  data = f.read().strip()


pages = []
for i in range(0, len(data), 2):
  pages.append((i // 2, int(data[i]), int(data[i+1]) if i + 1 < len(data) else 0))

full_length = sum(full + empty for _, full, empty in pages)
compressed_length = sum(full for _, full, _ in pages)

start = 0
end = 0

to_consume = []
for i, full, empty in pages:
  to_consume.append([i, full])
  to_consume.append([-1, empty])

to_consume.pop()

def consume_next():
  while to_consume and to_consume[0][1] == 0:
    to_consume.pop(0)

  i = to_consume[0][0]
  to_consume[0][1] -= 1
  consumed = i
  if i == -1:
    to_consume[-1][1] -=1
    consumed = to_consume[-1][0]
    if to_consume[-1][1] == 0:
      to_consume.pop()
    
    if to_consume[-1][0] == -1:
      to_consume.pop()
  
  if to_consume and to_consume[0][1] == 0:
    to_consume.pop(0)

  return consumed

checksum = 0

for index in range(compressed_length):
  next_i = consume_next()
  checksum += index * next_i

# pt 1
print(checksum)

to_consume = []
for i, full, empty in pages:
  to_consume.append([i, full])
  to_consume.append([-1, empty])

to_consume.pop()

for i, full, _ in pages[::-1]:
  index = to_consume.index([i, full])
  for dest, (oi, size) in enumerate(to_consume):
    if dest >= index:
      break
    if oi == -1 and full <= size:
      break
  if dest < index:
    to_consume.pop(index)
    if to_consume[index - 1][0] == -1:
      to_consume[index - 1][1] += full
      if index < len(to_consume) and to_consume[index][0] == -1:
        to_consume[index - 1][1] += to_consume[index][1]
        to_consume.pop(index)
    elif index < len(to_consume) and to_consume[index][0] == -1:
      to_consume[index][1] += full
    else:
      to_consume.insert(index, [-1, full])

    to_consume.insert(dest, [i, full])
    to_consume[dest + 1][1] -= full
    if to_consume[dest + 1][1] == 0:
      to_consume.pop(dest + 1)

#print("".join((str(i) if i >= 0 else ".") * size for i, size in to_consume))

checksum_2 = 0
index = 0
for i, size in to_consume:
  for _ in range(size):
    if i != -1:
      checksum_2 += i * index
    index += 1

print(checksum_2)