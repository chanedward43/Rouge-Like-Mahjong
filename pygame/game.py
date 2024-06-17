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

        self.round_num = 1
        self.discard_num = 3
        self.play_num = 3
        self.score = 0
        self.score_multiplier = 1000
        self.action = None  # 'play' or 'discard'
        self.discard_indices = []

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
            self.clock.tick(30)  # Limit the frame rate

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to play hand
                    self.action = 'play'
                elif event.key == pygame.K_d:  # Press 'D' to discard
                    self.action = 'discard'
                elif event.key == pygame.K_RETURN and self.action == 'discard':
                    self.discard_tiles()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.action == 'discard':
                    self.handle_tile_selection(event.pos)
                else:
                    self.handle_button_click(event.pos)

    def update(self):
        if self.action == 'play':
            self.handle_play()
            self.action = None  # Reset action after play
        elif self.action == 'discard':
            pass  # Discard action handled in handle_events

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.display_hand()
        self.display_game_info()
        self.display_buttons()
        pygame.display.flip()

    def display_hand(self):
        y = 500
        x_offset = 50
        for i, tile in enumerate(self.player.tiles):
            self.screen.blit(tile.image, (x_offset + i * 50, y))

    def display_game_info(self):
        info_text = [
            f"Round: {self.round_num}",
            f"Score: {self.score}",
            f"Required Score: {self.round_num * self.score_multiplier}",
            f"Play Chances: {self.play_num}",
            f"Discard Chances: {self.discard_num}",
            f"Deck: {len(self.deck)} tiles left",
        ]
        for i, text in enumerate(info_text):
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (50, 50 + i * 40))

    def display_buttons(self):
        play_button = pygame.Rect(600, 50, 150, 50)
        discard_button = pygame.Rect(600, 150, 150, 50)
        
        pygame.draw.rect(self.screen, (0, 128, 0), play_button)
        pygame.draw.rect(self.screen, (128, 0, 0), discard_button)
        
        play_text = self.font.render("Play", True, (255, 255, 255))
        discard_text = self.font.render("Discard", True, (255, 255, 255))
        
        self.screen.blit(play_text, (625, 60))
        self.screen.blit(discard_text, (610, 160))
        
        if self.action == 'discard':
            discard_indices_text = self.font.render(f"Selected: {self.discard_indices}", True, (0, 0, 0))
            self.screen.blit(discard_indices_text, (50, 450))

    def handle_play(self):
        scoring = Scoring(self.player)
        round_score = scoring.calculate_score()
        self.score += round_score

        if self.score >= self.round_num * self.score_multiplier:
            self.advance_round()
        elif self.play_num > 1:
            self.play_num -= 1
            self.start_new_round()
        else:
            print(f"You scored {self.score} out of {self.round_num * self.score_multiplier} points.")
            self.running = False

    def advance_round(self):
        print(f"Congratulations! You scored {self.score} points this round!")
        self.round_num += 1
        self.score = 0
        self.play_num = 3
        self.discard_num = 3
        self.start_new_round()

    def handle_button_click(self, mouse_pos):
        play_button = pygame.Rect(600, 50, 150, 50)
        discard_button = pygame.Rect(600, 150, 150, 50)
        
        if play_button.collidepoint(mouse_pos):
            self.action = 'play'
        elif discard_button.collidepoint(mouse_pos):
            self.action = 'discard'

    def handle_tile_selection(self, mouse_pos):
        y = 500
        x_offset = 50
        for i, tile in enumerate(self.player.tiles):
            tile_rect = pygame.Rect(x_offset + i * 50, y, tile.image.get_width(), tile.image.get_height())
            if tile_rect.collidepoint(mouse_pos):
                if i in self.discard_indices:
                    self.discard_indices.remove(i)
                else:
                    self.discard_indices.append(i)

    def discard_tiles(self):
        if len(self.discard_indices) > 0 and self.discard_num > 0:
            self.discard_indices.sort(reverse=True)
            for index in self.discard_indices:
                self.remove_tile(self.player.tiles[index])
                self.add_tile()
            self.discard_indices.clear()
            self.discard_num -= 1
        self.action = None

if __name__ == "__main__":
    game = Game()
    game.play_game()
    pygame.quit()