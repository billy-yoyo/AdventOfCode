from collections import defaultdict

with open("input") as f:
    input = f.read()

alphabet = "abcdefghijklmnopqrstuvwxyz"
def rotate(letter, amount):
    index = alphabet.index(letter)
    return alphabet[(index + amount) % len(alphabet)]

def read_room(line):
    name, checksum = line.split("[")
    checksum = checksum[:-1]
    name_parts = name.split("-")
    name, sector_id = "-".join(name_parts[:-1]), int(name_parts[-1])
    letters = defaultdict(int)
    for letter in name:
        if letter != "-":
            letters[letter] += 1
    sorted_letters = sorted([(-x[1], x[0]) for x in letters.items()])
    letter_checksum = "".join(x[1] for x in sorted_letters)
    if letter_checksum.startswith(checksum):
        return "".join([
            letter if letter == "-" else rotate(letter, sector_id) for letter in name
        ]), sector_id
    return None, None

for line in input.strip().split("\n"):
    room_name, sector_id = read_room(line)
    if room_name and "north" in room_name:
        print(room_name, sector_id)
