import math

M = 20201227
M_sqrt = math.ceil(math.sqrt(M))

def hash(a, secret):
    return pow(a, secret, M)


def unhash(a, b):
    table = {}
    for j in range(M_sqrt):
        aj = pow(a, j, M)
        table[aj] = j

    m_inv = pow(a, M-M_sqrt-1, M)
    print(m_inv)
    g = b
    for i in range(M_sqrt):
        if g in table:
            return (i * M_sqrt) + table[g]
        g = (g * m_inv) % M
    
    return None

card_key = 2069194
door_key = 16426071



card_secret = unhash(7, card_key)
door_secret = unhash(7, door_key)

print(f"card_secret={card_secret}")
print(f"door_secret={door_secret}")

assert hash(7, card_secret) == card_key
assert hash(7, door_secret) == door_key

encryption_key = hash(card_key, door_secret)
print(encryption_key)