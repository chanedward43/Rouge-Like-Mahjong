import random
from tile import Tile
from hand import Hand

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
        score = 0
        while True:
            not_played = True
            print(f"\n=== Round {round_num} ===")

            while not_played:
                if discard_num != 0:
                    self.display_hand()
                    print(f"Discard chances: {discard_num}")
                    print(f"Deck: {len(self.deck)} tiles left")
                    action = input("Enter 'play' to play your hand or 'discard' to discard tiles: ").strip().lower()
                else:
                    action = 'play'
                
                if action == 'play':
                    score = 1  # Simulate a winning condition
                    if score == 1:
                        print("\nCongratulations! You won this round!")
                        score = 0
                        not_played = False
                        discard_num = 3
                        self.start_new_round()
                        round_num += 1
                        break
                    else:
                        print("Sorry, you lost this round.")
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