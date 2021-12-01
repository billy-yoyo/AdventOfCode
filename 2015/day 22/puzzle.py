
class Effect:
    def __init__(self, name, turns, cb, end_cb=None, start_cb=None):
        self.name = name
        self.turns = turns
        self.cb = cb
        self.end_cb = end_cb
        self.start_cb = start_cb

    def run(self, state):
        self.turns -= 1
        self.cb(state, self.turns)

    def clone(self):
        return Effect(self.name, self.turns, self.cb, self.end_cb, self.start_cb)

class Character:
    def __init__(self, hp, armour, dmg):
        self.hp = hp
        self.armour = armour
        self.dmg = dmg

    def hit(self, dmg):
        self.hp -= max(1, dmg - self.armour)
        return self

    def heal(self, hp):
        self.hp += hp
        return self

    def shield(self, armour):
        self.armour += armour
        return self

    def clone(self):
        return Character(self.hp, self.armour, self.dmg)

class State:
    def __init__(self):
        self.mana = 500
        self.player = Character(50, 0, 0)
        self.boss = Character(51, 0, 9)
        self.effects = []
        self.history = []
        self.spent = 0

    def clone(self):
        state = State()
        state.mana = self.mana
        state.player = self.player.clone()
        state.boss = self.boss.clone()
        state.effects = [e.clone() for e in self.effects]
        state.history = self.history[:]
        state.spent = self.spent
        return state

    def add_history(self, text):
        self.history.append(text)
        return self

    def restore_mana(self, amount):
        self.mana += amount
        return self

    def spend_mana(self, mana):
        if self.mana >= mana:
            self.mana -= mana
            self.spent += mana
            return True
        return False

    def do_effects(self):
        new_effects = []
        for effect in self.effects:
            effect.run(self)
            if effect.turns > 0:
                new_effects.append(effect)
            elif effect.end_cb:
                effect.end_cb(self)
        self.effects = new_effects

    def check_player_dead(self):
        return self.player.hp <= 0
    
    def check_boss_dead(self):
        return self.boss.hp <= 0


class Spell:
    def __init__(self, name, mana, effect_turns, cb, start_cb=None, end_cb=None):
        self.name = name
        self.mana = mana
        self.effect_turns = effect_turns
        self.cb = cb
        self.start_cb = start_cb
        self.end_cb = end_cb
    
    def run(self, state):
        if state.spend_mana(self.mana):
            if self.effect_turns > 0:
                if self.start_cb:
                    self.start_cb(state)
                state.effects.append(Effect(self.name, self.effect_turns, self.cb, start_cb=self.start_cb, end_cb=self.end_cb))
            else:
                self.cb(state)
            return True
        return False

spells = [
    Spell("Magic Missile", 53, 0, lambda s: s.boss.hit(4) and s.add_history("Player casts Magic Missile, dealing 4 damage")),
    Spell("Drain", 73, 0, lambda s: s.boss.hit(2) and s.player.heal(2) and s.add_history("Player casts Drain, dealing 2 damage, and healing 2 hit points")),
    Spell("Shield", 113, 6, lambda s,t: s.add_history(f"Shield's timer is now {t}"), start_cb=lambda s: s.player.shield(7) and s.add_history("Player casts Shield, increasing armour by 7"), end_cb=lambda s: s.player.shield(-7) and s.add_history("Shield wears off, decreasing armor by 7")),
    Spell("Poison", 173, 6, lambda s,t: s.boss.hit(3) and s.add_history(f"Poison dealt 3 damage; its timer is now {t}."), start_cb=lambda s: s.add_history("Player casts Poison"), end_cb=lambda s: s.add_history("Poison wears off")),
    Spell("Recharge", 229, 5, lambda s,t: s.restore_mana(101) and s.add_history(f"Recharge provides 101 mana; its timer is now {t}."), start_cb=lambda s: s.add_history("Player casts Recharge"), end_cb=lambda s: s.add_history("Recharge wears off"))
]

min_spell_cost = min(spell.mana for spell in spells)

class Cache:
    def __init__(self):
        self.best = None

cache = Cache()

def do_turn(state, spell):
    if cache.best and state.spent > cache.best.spent:
        return

    # player turn
    state.add_history("\n-- Player turn --")
    state.add_history(f"- Player has {state.player.hp} hit points, {state.player.armour} armour, {state.mana} mana")
    state.add_history(f"- Boss has {state.boss.hp} hit points")
    state.player.hp -= 1
    if state.check_player_dead():
        return

    state.do_effects()
    if state.check_boss_dead():
        state.add_history("boss dead")
        yield state
        return
    
    if not spell.run(state):
        return
    
    if state.check_boss_dead():
        state.add_history("boss dead")
        yield state
        return 
    
    # boss turn

    state.add_history("\n--- Boss turn ---")
    state.add_history(f"- Player has {state.player.hp} hit points, {state.player.armour} armour, {state.mana} mana")
    state.add_history(f"- Boss has {state.boss.hp} hit points")
    state.do_effects()

    if state.check_boss_dead():
        state.add_history("boss dead")
        yield state
        return 
    
    state.add_history(f"player hit for {state.boss.dmg}, deals {max(1, state.boss.dmg - state.player.armour)} damage")
    state.player.hit(state.boss.dmg)

    if state.check_player_dead():
        return

    for next_spell in spells:
        # can't cast a spell already in effect
        if next_spell.effect_turns > 0 and any(e.name == next_spell.name and e.turns > 1 for e in state.effects):
            continue
        yield from do_turn(state.clone(), next_spell)

def do_game():
    for spell in spells:
        yield from do_turn(State(), spell)

costs = []

for state in do_game():
    costs.append(state.spent)
    if cache.best is None or state.spent < cache.best.spent:
        cache.best = state

print("\n".join(cache.best.history))
print(cache.best.spent)