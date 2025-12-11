from hashlib import md5

offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
directions = "UDLR"
open_chars = "bcdef"

def find_path(key):
    state = [(0, 0, "")]
    best_path = None
    while state:
        next_state = []
        for x, y, path in state:
            if x == 3 and y == 3:
                best_path = path
                continue
            hash = md5(f"{key}{path}".encode()).hexdigest()[:4]
            for i, (ox, oy) in enumerate(offsets):
                nx, ny = x + ox, y + oy
                if 0 <= nx < 4 and 0 <= ny < 4 and hash[i] in open_chars:
                    next_state.append((nx, ny, path + directions[i]))
        state = next_state
    return best_path
    

print(len(find_path("bwnlcvfs")))