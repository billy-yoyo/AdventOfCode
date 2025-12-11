
with open("puzzle") as f:
    data = f.read().strip()

score_map = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

outcome_map = {
    "A": {
        "X": 3,
        "Y": 6,
        "Z": 0
    },
    "B": {
        "X": 0,
        "Y": 3,
        "Z": 6
    },
    "C": {
        "X": 6,
        "Y": 0,
        "Z": 3
    }
}

outcome_map_2 = {
    "A": {
        "X": 3,
        "Y": 4,
        "Z": 8
    },
    "B": {
        "X": 1,
        "Y": 5,
        "Z": 9
    },
    "C": {
        "X": 2,
        "Y": 6,
        "Z": 7
    }
}

def score(left, right):
    return score_map[right] + outcome_map[left][right]

def score2(left, right):
    return outcome_map_2[left][right]

rounds = [r.split() for r in data.split("\n")]

print(sum(score2(*r) for r in rounds))
