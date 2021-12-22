
def overlap(p1, p2):
    return p1[0] <= p2[1] and p2[0] <= p1[1]

def inside(p1, p2):
    return p2[0] <= p1[0] and p1[1] <= p2[1]

    