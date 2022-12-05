
from collections import defaultdict
import time

with open("testinput") as f:
    input = f.read()

input = input.strip().split("\n")

room_positions = [
    [(3, 2), (3, 3)],
    [(5, 2), (5, 3)],
    [(7, 2), (7, 3)],
    [(9, 2), (9, 3)],
]

room_map = "ABCD"

score_map = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

rooms = [
    [input[y][x] for x, y in room] for room in room_positions
]

spaces = [None, None, None, None, None]

def calculate_hash():
    return tuple(tuple(room) for room in rooms) + tuple(spaces)

cache = {}

class Best:
    def __init__(self):
        self.score = None

best = Best()

def play(score=0, check=False):
    print(f"{spaces} :: {rooms}")
    #print(spaces)
    #time.sleep(1)
    if best.score is not None and score > best.score:
        #print("culling because score is too high")
        return

    # who can move out of their room
    # a room is encoded as (0, room_index, space_index)
    # a hallway is encoded as (1, space_index)
    #hash = calculate_hash()
    #if hash in cache and cache[hash] < score:
        #print("cache collision")
    #    return
    
    #cache[hash] = score
    
    if check and all(all(x == "ABCD"[i] for x in room) for i, room in enumerate(rooms)):
        #print(f"finished path with new score {score}")
        if best.score is None or score < best.score:
            print(f"new best score is {score}")
            best.score = score

    # N N N
    #  A A
    for i, space in enumerate(spaces):
        if space is not None:
            available_rooms = []
            ni = i - 1
            steps = 2
            while ni >= 0 and (ni + 1 == i or spaces[ni + 1] is None):
                if rooms[ni][0] is None:
                    ri = 0
                elif rooms[ni][1] is None:
                    ri = 1
                else:
                    ri = 2
                
                if ri < 2 and (ri == 1 or rooms[ni][1] == room_map[ni]) and room_map[ni] == space:
                    available_rooms.append((ni, ri, steps + ri))
                
                steps += 2
                ni -= 1
                
            pi = i
            steps = 2
            while pi < len(rooms) and (pi == i or spaces[pi] is None):
                if rooms[pi][0] is None:
                    ri = 0
                elif rooms[pi][1] is None:
                    ri = 1
                else:
                    ri = 2
                
                if ri < 2 and (ri == 1 or rooms[pi][1] == room_map[pi]) and room_map[pi] == space:
                    available_rooms.append((pi, ri, steps + ri))
                
                steps += 2
                pi += 1
            
            for ci, ri, steps in available_rooms:
                #print(f"moving {space} from space {i} to room {ci} (target: {room_map[ci]})")
                spaces[i] = None
                rooms[ci][ri] = space
                play(score + (steps * score_map[space]), check=True)
                spaces[i] = space
                rooms[ci][ri] = None

    for i, room in enumerate(rooms):
        room_index = 0
        if room[0] is not None:
            room_index = 0
        elif room[1] is not None:
            room_index = 1
        else:
            continue

        # this room is already complete, don't move any out of it
        if room_index == 0 and room[0] == room_map[i] and room[1] == room_map[i]:
            continue

        # this letter is in the correct position, dont move it
        if room_index == 1 and room[1] == room_map[i]:
            continue

        available_spaces = []
        ni = i
        steps = 2
        while ni >= 0 and spaces[ni] is None:
            available_spaces.append((ni, steps))
            steps += 2
            ni -= 1
        pi = i + 1
        steps = 2
        while pi < len(spaces) and spaces[pi] is None:
            available_spaces.append((pi, steps))
            steps += 2
            pi += 1
        
        for space, steps in available_spaces:
            letter = room[room_index]
            room[room_index] = None
            spaces[space] = letter
            play(score + (score_map[letter] * (steps + room_index)))
            room[room_index] = letter
            spaces[space] = None

play()
print(best.score)