
class Game:
    def __init__(self, players):
        self.players = players
        self.history = set()

    def check_history(self):
        state = ";".join(",".join(str(x) for x in player) for player in self.players)
        if state in self.history:
            return False
        self.history.add(state)
        return True

    def play_round(self):
        # end game via recursion
        if not self.check_history():
            return True, 0

        left, right = [deck.pop(0) for deck in self.players]

        # play recursive combat
        if len(self.players[0]) >= left and len(self.players[1]) >= right:
            sub_game = Game([self.players[0][:left], self.players[1][:right]])
            winner = sub_game.play_game()

            if winner == 0:
                self.players[0] += [left, right]
            else:
                self.players[1] += [right, left]
        else:
            if left > right:
                self.players[0] += [left, right]
            else:
                self.players[1] += [right, left]

        if len(self.players[0]) == 0:
            return True, 1
        elif len(self.players[1]) == 0:
            return True, 0
        else:
            return False, None

    def play_game(self):
        finished, winner = self.play_round()
        while not finished:
            finished, winner = self.play_round()

        return winner

    def calculate_score(self, player):
        return sum ((i + 1) * x for i, x in enumerate(reversed(self.players[player])))

with open("data") as f:
    player_strings = f.read().strip().split("\n\n")
    game = Game([
        [int(x.strip()) for x in player.strip().split("\n")[1:] if x.strip()] for player in player_strings if player.strip()
    ])

winner = game.play_game()
print(game.calculate_score(winner))