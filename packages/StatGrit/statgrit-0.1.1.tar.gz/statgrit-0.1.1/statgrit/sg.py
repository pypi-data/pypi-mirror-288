class GameScoreTracker:
    def __init__(self):
        self.scores = {}

    def add_player(self, player_name):
        if player_name in self.scores:
            print(f"Player {player_name} already exists.\n")
        else:
            self.scores[player_name] = 0
            print(f"Player {player_name} added.\n")

    def remove_player(self, player_name):
        if player_name in self.scores:
            del self.scores[player_name]
            print(f"Player {player_name} removed.\n")
        else:
            print(f"Player {player_name} does not exist.\n")

    def update_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
            print(f"Player {player_name}'s score updated to {self.scores[player_name]}.\n")
        else:
            print(f"Player {player_name} does not exist. Please add the player first.\n")

    def get_score(self, player_name):
        return self.scores.get(player_name, None)

    def get_all_scores(self):
        return self.scores

# Automatically display some information when the module is imported
if __name__ == "__main__":
    tracker = GameScoreTracker()
    print("StatGrit GameScoreTracker initialized!\n")
else:
    print("StatGrit GameScoreTracker module imported!\n")
