

with open("passports.txt") as f:
    passports = [{key: value for key, value in [field.split(":") for field in passport.split()]} for passport in f.read().split("\n\n")]

def is_int(n):
    try:
        int(n)
        return True
    except:
        return False

height_validators = {
    "cm": lambda v: is_int(v) and 150 <= int(v) <= 193,
    "in": lambda v: is_int(v) and 59 <= int(v) <= 76
}
hexalpha = "0123456789abcdef"

required_fields = [
    ("byr", lambda v: len(v) == 4 and is_int(v) and 1920 <= int(v) <= 2002), 
    ("iyr", lambda v: len(v) == 4 and is_int(v) and 2010 <= int(v) <= 2020), 
    ("eyr", lambda v: len(v) == 4 and is_int(v) and 2020 <= int(v) <= 2030), 
    ("hgt", lambda v: v[-2:] in height_validators and height_validators[v[-2:]](v[:-2])), 
    ("hcl", lambda v: v[0] == "#" and all(c in hexalpha for c in v[1:])), 
    ("ecl", lambda v: v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]), 
    ("pid", lambda v: len(v) == 9 and is_int(v))
]
valid_passports = 0
for passport in passports:
    if all(field in passport and validator(passport[field]) for field, validator in required_fields):
        valid_passports += 1
print(valid_passports)
