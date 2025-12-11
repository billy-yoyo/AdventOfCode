from functools import cache
import time

p = [3, 7]
d = [0, 0]
s = [0, 0]

def roll():
    value = d[0] + 1
    d[0] = (d[0] + 1) % 100
    d[1] += 1
    return value

def play_turn(i):
    p[i] = (p[i] + roll() + roll() + roll()) % 10
    s[i] += p[i] + 1
    #print(f"Player {i} moves to space {p[i]} for a total score of {s[i]}")

turn = 0
while s[0] < 21 and s[1] < 21:
    play_turn(turn)
    turn = (turn + 1) % 2

# 1 + 1 + 3
# 1 + 2 + 2

# outcomes:
# 3 (1/27)
# 4 (3/27)
# 5 (6/27)
# 6 (7/27)
# 7 (6/27)
# 8 (3/27)
# 9 (1/27)

outcomes = [[3, 1], [4, 3], [5, 6], [6, 7], [7, 6], [8, 3], [9, 1]]

def count_wins(p1, p2, s1, s2, turn):
    for outcome, freq in outcomes:
        np1, np2, ns1, ns2 = p1, p2, s1, s2
        if turn == 0:
            np1 = (p1 + outcome) % 10
            ns1 += np1 + 1
        else:
            np2 = (p2 + outcome) % 10
            ns2 += np2 + 1
        
        if ns1 >= 21:
            yield (freq, 0)
        elif ns2 >= 21:
            yield (0, freq)
        else:
            tw1, tw2 = 0, 0
            for w1, w2 in count_wins(np1, np2, ns1, ns2, (turn + 1) % 2):
                tw1 += w1
                tw2 += w2
            yield (tw1 * freq, tw2 * freq)

start_time = time.time()
tw1, tw2 = 0, 0
for w1, w2 in count_wins(5, 9, 0, 0, 0):
    tw1 += w1
    tw2 += w2
print(f"tookn {time.time() - start_time} seconds")

print(tw1, tw2)
print(min(tw1, tw2))

