from collections import deque

total_players, total_marbles = 476, 71431 * 100
#total_players, total_marbles = 10, 1618
#total_players, total_marbles = 9, 25

def calc(total_players, total_marbles):
    scores = [0] * total_players
    stack = deque([0, 1])
    for i in range(2, total_marbles + 1):
        if i % 23 == 0:
            stack.rotate(7)
            scores[i % total_players] += i + stack.pop()
            stack.rotate(-1)
        else:
            stack.rotate(-1)
            stack.append(i)
    print(max(scores))

calc(total_players, total_marbles)