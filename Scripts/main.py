import random
from tile import Tile
from hand import Hand
from scoring import Scoring

class Game:
    def __init__(self):
        self.suits = ['bam', 'cir', 'cha']  # bamboo, circle, character
        self.specials = ['east', 'south', 'west', 'north', 'white', 'green', 'red']
        self.player = Hand()
        self.start_new_round()

    def create_deck(self):
        deck = []
        for suit in self.suits:
            for value in range(1, 10):
                for _ in range(4):
                    deck.append(Tile(suit, str(value)))  # Ensure value is a string
        for special in self.specials:
            for _ in range(4):
                deck.append(Tile('special', special))
        random.shuffle(deck)
        return deck

    def distribute_tiles(self):
        for _ in range(14):
            self.player.add_tile(self.deck.pop())

    def start_new_round(self):
        self.deck = self.create_deck()
        self.player.clear_tiles()
        self.distribute_tiles()

    def add_tile(self):
        self.player.add_tile(self.deck.pop())

    def remove_tile(self, tile):
        self.player.remove_tile(tile)

    def play_game(self):
        round_num = 1
        discard_num = 3
        play_num = 3
        score = 0
        score_multiplier = 1000
        while True:
            not_played = True
            print(f"\n=== Round {round_num} | You need to score {round_num * score_multiplier} to Win ===")

            while not_played:
                self.display_hand()
                print(f"Deck: {len(self.deck)} tiles left")
                print(f"Discard chances: {discard_num}")
                print(f"Play chances: {play_num}")
                if discard_num != 0:
                    action = input("Enter 'play' to play your hand or 'discard' to discard tiles: ").strip().lower()
                else:
                    action = 'play'

                if action == 'play':
                    scoring = Scoring(self.player)
                    score += scoring.calculate_score()
                    if score >= score_multiplier * round_num:
                        print(f"\nCongratulations! You scored {score} points this round!")
                        not_played = False
                        discard_num = 3
                        play_num = 3
                        self.start_new_round()
                        round_num += 1
                        score = 0
                        break
                    elif play_num != 1:
                        self.start_new_round()
                        play_num -= 1
                        print(f"\nYou scored {score} out of {round_num * score_multiplier} points. You have {play_num} more chances to play.")
                        print(f"\n=== Round {round_num} | You need to score {round_num * score_multiplier - score} to Win ===")
                    else:
                        print(f"You scored {score} out of {round_num * score_multiplier} points. You need {score_multiplier * round_num - score} more points to win.")
                        return
                elif action == 'discard':
                    self.display_hand()
                    print(f"Deck: {len(self.deck)} tiles left")

                    discard_indices = self.get_valid_discard_indices()

                    discard_indices.sort(reverse=True)  # Sort in reverse order to avoid index shift issues
                    for index in discard_indices:
                        tile_to_remove = self.player.tiles[index - 1]  # Convert to zero-based index
                        self.remove_tile(tile_to_remove)
                        self.add_tile()
                    discard_num -= 1

    def display_hand(self):
        print("\n--- Player's Hand ---")
        for i, tile in enumerate(self.player.tiles, start=1):
            print(f"{i}: {tile}")

    def get_valid_discard_indices(self):
        while True:
            tile_input = input("Enter the numbers of the tiles you want to discard (e.g., '1 2'): ").strip()
            try:
                discard_indices = [int(index) for index in tile_input.split()]
                if len(discard_indices) != len(set(discard_indices)):
                    print("Duplicate indices detected. Please enter unique indices.")
                    continue
                if all(1 <= index <= len(self.player.tiles) for index in discard_indices):
                    return discard_indices
                else:
                    print("Invalid indices detected. Please enter indices within the valid range.")
            except ValueError:
                print("Invalid input format. Please enter numbers separated by spaces.")

if __name__ == "__main__":
    game = Game()
    game.play_game()