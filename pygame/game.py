import os
import pygame
import random
from tile import Tile
from hand import Hand
from scoring import Scoring

# Ensure the working directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mahjong Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        
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
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Update game logic here
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.display_hand()
        pygame.display.flip()

    def display_hand(self):
        y = 500
        x_offset = 50
        for i, tile in enumerate(self.player.tiles):
            self.screen.blit(tile.image, (x_offset + i * 50, y))

if __name__ == "__main__":
    game = Game()
    game.play_game()
    pygame.quit()
