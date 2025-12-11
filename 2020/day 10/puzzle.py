
branches = (lambda f,d:f(f,len(d)-1,{},d))(lambda f,p,m,d:m[p]if p in m else (lambda s: [m.update({p:s}),s][1])(sum(f(f,p-(i+1),m,d)for i,v in enumerate(d[p-1:max(0,p-4):-1])if v>=d[p]-3)+(d[p]<=3)),sorted(int(x)for x in open("data").read().split()if x))
print(branches)

with open("data") as f:
    adapters = sorted(int(x) for x in f.read().split() if x)

memoized = {}
def calculate_branches(pointer):
    if pointer in memoized:
        return memoized[pointer]
    
    value = adapters[pointer]
    branches = 0

    if value <= 3:
        branches += 1

    new_pointer = pointer - 1
    while new_pointer >= 0 and adapters[new_pointer] >= value - 3:
        branches += calculate_branches(new_pointer)
        new_pointer -= 1

    memoized[pointer] = branches
    return branches

branches = calculate_branches(len(adapters) - 1)
print(branches)