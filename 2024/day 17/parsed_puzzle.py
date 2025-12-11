
A = 1283019283102398

def calc(A):
  B = (A % 8)^2
  C = A // (2 ** B)
  return ((B ^ C) ^ 3) % 8

inout_short = [calc(x) for x in range(8)]

inout = []
i = 0
while i == 0 or len(inout) % 2 != 0 or inout[:len(inout)//2] != inout[len(inout)//2:]:
  inout.append(calc(i))
  i += 1

inout = inout[:len(inout)//2]

output = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]
inputs = [inout.index(out) for out in output]

possibilities = [[i for i, x in enumerate(inout) if x == out] for out in output]

def matches(val, output):
  for out in output:
    if calc(val) != out:
      return False
    val //= 8
  return True

# first 8 
As = [0]
for x in output[::-1]:
  next_As = []
  for i in range(8):
    for A in As:
      next_A = (A * 8) + i
      if calc(next_A) == x:
        next_As.append(next_A)
  As = next_As

print(min(As))

i = 0
while True:
  break
  if i % 100000 == 0:
    print(i)
  
  for x in possibilities[-1]:
    if matches(x+(i*1024), output):
      print(x+(i*1024))
      break
  i += 1


#print(possible)
#print(8 ** (len(output) - 1))

#start = 8 ** (len(output) - 1)

# A = i1 + d*1024
# d = (A - i1)/1024
# d = ((A//8) - i2)/1024

# A % 1024 == i1
# (A // 8) % 1024 == i2
# (A // 16) % 1024 == i3



# f(A) == 2
# f(A // 8) == 4
# f(A // 16) == 1
# ...

