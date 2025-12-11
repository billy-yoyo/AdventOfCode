from hashlib import md5

door_id = "ugkcyxxp"
password = [None] * 8

i = 0
while any(x is None for x in password):
    hash = md5((door_id + str(i)).encode("utf-8")).hexdigest()
    if hash.startswith("00000"):
        if hash[5] in "01234567":
            index = int(hash[5])
            if password[index] is None:
                print(f"{i}: {hash}")
                password[index] = hash[6]
    i += 1

print("".join(password))
