
def combo(f):
  return lambda regs, x: f(regs, x if x <= 3 else regs[x-4])

A = 0
B = 1
C = 2


SET = "SET"
JUMP = "JUMP"
VOID = "VOID"
OUTPUT = "OUTPUT"

def setreg(reg, value):
  return (SET, reg, value)

def jump(value):
  return (JUMP, None, value)

def void():
  return (VOID, None, None)

def output(value):
  return (OUTPUT, None, value)

opcodes = [
  ("adv", "A = A // 2**{x}", combo(lambda regs, x: setreg(A, regs[A] / (2 ** x)))),
  ("bxl", "B = B ^ {x}", lambda regs, x: setreg(B, regs[B] ^ x)),
  ("bst", "B = {x} % 8", combo(lambda _, x: setreg(B, x % 8))),
  ("jnz", "jump({x})", lambda regs, x: void() if regs[A] == 0 else jump(x)),
  ("bxc", "B = B ^ C", lambda regs, _: setreg(B, regs[B] ^ regs[C])),
  ("out", "out({x} % 8)", combo(lambda _, x: output(x % 8))),
  ("bdv", "B = A // 2**{x}", combo(lambda regs, x: setreg(B, regs[A] / (2 ** x)))),
  ("cdv", "C = A // 2**{x}", combo(lambda regs, x: setreg(C, regs[A] / (2 ** x)))),
]

def compile_program(program):
  code = []
  pointer = 0
  while pointer < len(program):
    opcode, operand = program[pointer], program[pointer + 1]
    pointer += 2
    name = opcodes[opcode][1]

    if name not in ("bxl", "jnz", "bxc") and operand >= 4 and operand < 7:
      operand = "ABC"[operand - 4]

    code.append(name.format(x=operand) + "\n")
  
  with open("code", "w") as f:
    f.writelines(code)

def execute_program(regs, program):
  regs = list(regs)
  outputs = []

  pointer = 0
  while pointer < len(program):
    opcode, operand = program[pointer], program[pointer + 1]
    pointer += 2
    code, reg, value = opcodes[opcode][2](regs, operand)
    if code == SET:
      regs[reg] = int(value)
    elif code == JUMP:
      pointer = value
    elif code == OUTPUT:
      outputs.append(value)
  
  return outputs

with open("data") as f:
  regstring, progstring = f.read().strip().split("\n\n")

regs = [int(reg.split(":")[1].strip()) for reg in regstring.split("\n")]
program = [int(x.strip()) for x in progstring.split(":")[1].strip().split(",")]

#print(regs)
#print(program)

#print(",".join([str(x) for x in execute_program(regs, program)]))

#print(compile_program(program))

#for i in range(1024):
#  out = execute_program([35184372088832 + i] + regs[1:], program)
#  print(out )

print(execute_program([37221274271220] + regs[1:], program))

#i = 0
#while True:
#  if execute_program([i] + regs[1:], program, program) is not None:
#    print(i)
#    break
#  i += 1
