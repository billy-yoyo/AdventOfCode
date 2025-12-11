from collections import defaultdict

def score_card(card):
    return "J23456789TQKA".index(card)

def score_hand(hand):
    counts = defaultdict(int)
    for x in hand:
        counts[x] += 1

    FIVE = 100
    FOUR = 90
    FULL_HOUSE = 80
    THREE = 70
    TWO_PAIR = 60
    ONE_PAIR = 50
    HIGH_CARD = 40

    if len(counts) == 1: # AAAAA
        return 100 # 5-kind (11111)
    elif len(counts) == 2: # AAAAB | AAABB 
        if any(x == 4 for x in counts.values()):
            if any(x == "J" for x in counts.keys()):
                return FIVE # 5-kind (J1111) | (1JJJJ)
            else:
                return FOUR # 4-kind (?1111)
        elif any(x == "J" for x in counts.keys()):
            return FIVE # 5-kind (JJ111) | (11JJJ)
        else:
            return FULL_HOUSE # full-house (11122)
    elif len(counts) == 3: # AAABC | AABBC 
        if any(x == 3 for x in counts.values()):
            if any(x == "J" for x in counts.keys()):
                return FOUR # 4-kind (111J?) | (JJJ1?)
            else:
                return THREE # 3-kind (111??)
        else:
            pair_a, pair_b = [x for x in counts.keys() if counts[x] == 2]
            if pair_a == "J" or pair_b == "J":
                return 90 #  (11JJ?)
            elif any(x == "J" for x in counts.keys()):
                return FULL_HOUSE # (1122J)
            else:
                return TWO_PAIR # 2-pair (1122?)
    elif len(counts) == 4: # AABCD
        if any(x == "J" for x in counts.keys()):
            return THREE # 3-kind (JJ1??) | (11J??)
        else:
            return ONE_PAIR # 1-pair
    elif any(x == "J" for x in counts.keys()): # ABCDE
        return ONE_PAIR # 1-pair
    else: # ABCDE
        return HIGH_CARD

def pad(x):
    if x < 10:
        return "0" + str(x)
    else:
        return str(x)

def tiebreak_hand(hand):
    return "".join([pad(score_card(card)) for card in hand])

with open("input") as f:
    bids = [(x, int(y)) for x, y in [l.split() for l in f.read().strip().split("\n")]]
    bids = sorted(bids, key=lambda p: (score_hand(p[0]), tiebreak_hand(p[0])))
    print([(p[0], score_hand(p[0])) for p in bids])
    total = 0
    for i, (_, bid) in enumerate(bids):
        total += (i + 1) * bid
    print(total)
        
