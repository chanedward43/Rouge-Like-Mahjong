import random
from tile import Tile
from hand import Hand

class Game:
    def __init__(self):
        self.suits = ['bam', 'cir', 'cha']  # bamboo, circle, character
        self.specials = ['east', 'south', 'west', 'north', 'white', 'green', 'red']
        self.deck = self.create_deck()
        self.player = Hand()
        self.distribute_tiles()

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

    def add_tile(self):
        self.player.add_tile(self.deck.pop())

    def remove_tile(self, tile):
        self.player.remove_tile(tile)

    def play_game(self):
        round_num = 1
        while len(self.deck) > 0:
            print(f"Round {round_num}")
            print("Player's hand: ")
            print(self.player)
            print("Deck: ")
            print(len(self.deck), "tiles left")
            print("Enter the tiles you want to discard (format: value suit, e.g., '1 bam, 2 cir'):")
            tile_input = input().strip()
            # Split input by comma, then strip each part and split by space
            discard_tiles = [part.strip().split() for part in tile_input.split(",")]
            for value, suit in discard_tiles:
                try:
                    tile_to_remove = Tile(suit, value)
                    if tile_to_remove in self.player.tiles:
                        self.remove_tile(tile_to_remove)
                        self.add_tile()
                    else:
                        print(f"Tile {value} {suit} not found in hand.")
                except ValueError:
                    print(f"Invalid tile format: {value} {suit}")
            round_num += 1

if __name__ == "__main__":
    game = Game()
    game.play_game()
