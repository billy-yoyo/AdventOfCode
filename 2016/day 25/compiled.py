

def iterates(X):
    next = 0
    a = X + 2550
    while a != 0:
        c = a % 2
        a //= 2
        if c != next:
            return False
        else:
            next = (next + 1) % 2
        a -= 1
    return True

X = 0
while not iterates(X):
    X += 1
print(X)
