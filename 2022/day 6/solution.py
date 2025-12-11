

with open("puzzle") as f:
    data = f.read()
    
#data = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

def get_start():
    for i in range(len(data)-14):
        if len(set(data[i:i+14])) == 14:
            return i + 14

print(get_start())
