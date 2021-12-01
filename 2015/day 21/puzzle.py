import math

class Item:
    def __init__(self, cost, dmg=0, armour=0):
        self.cost = cost
        self.dmg = dmg
        self.armour = armour

player_hp = 100
boss_hp = 109
boss_damage = 8
boss_armour = 2

weapons = [Item(8, 4), Item(10, 5), Item(25, 6), Item(40, 7), Item(74, 8)]
armours = [Item(0), Item(13, 0, 1), Item(31, 0, 2), Item(53, 0, 3), Item(75, 0, 4), Item(102, 0, 5)]
rings = [Item(0), Item(25, 1), Item(50, 2), Item(100, 3), Item(20, 0, 1), Item(40, 0, 2), Item(80, 0, 3)]

def does_player_win(player_dmg, player_armour):
    player_hit = max(1, player_dmg - boss_armour)
    boss_hit = max(1, boss_damage - player_armour)

    player_turns = math.ceil(boss_hp / player_hit)
    boss_turns = math.ceil(player_hp / boss_hit)
    return player_turns <= boss_turns

highest_total_cost = 0
for weapon in weapons:
    for armour in armours:
        for i, ring_1 in enumerate(rings):
            for j, ring_2 in enumerate(rings):
                if i == j:
                    continue
                total_cost = weapon.cost + armour.cost + ring_1.cost + ring_2.cost
                total_dmg = weapon.dmg + armour.dmg + ring_1.dmg + ring_2.dmg
                total_armour = weapon.armour + armour.armour + ring_1.armour + ring_2.armour
                if (highest_total_cost == 0 or total_cost > highest_total_cost) and not does_player_win(total_dmg, total_armour):
                    print(f"weapon={weapon.dmg} armour={armour.armour} ring1=({ring_1.dmg}, {ring_1.armour}) ring2=({ring_2.dmg}, {ring_2.armour})")
                    highest_total_cost = total_cost

print(highest_total_cost)