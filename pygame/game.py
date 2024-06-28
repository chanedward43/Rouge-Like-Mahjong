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
        self.width, self.height = 1200, 1000
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
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
                if event.key == pygame.K_q and self.action != 'discard':  # Press 'Q' to play hand
                    self.action = 'play'
                elif event.key == pygame.K_w:  # Press 'W' to discard
                    self.action = 'discard'
                elif event.key == pygame.K_e and self.action == 'discard':  # Press 'E' to confirm discard
                    self.discard_tiles()
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
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
        y = self.height - int(self.height * 0.1)
        x_offset = int(self.width * 0.08)
        tile_width = int(self.width * 0.05)
        tile_height = int(self.height * 0.15)
        spacing = int(tile_width * 0.2)  # Add some spacing between tiles
        selected_scale_factor = 1.15  # Scale factor for selected tiles

        for i, tile in enumerate(self.player.tiles):
            tile_rect = pygame.Rect(x_offset + i * (tile_width + spacing), y, tile_width, tile_height)
            
            if i in self.discard_indices:
                # Selected tiles are scaled larger
                larger_tile_image = pygame.transform.scale(tile.image, (int(tile_width * selected_scale_factor), int(tile_height * selected_scale_factor)))
                self.screen.blit(larger_tile_image, (tile_rect.x, tile_rect.y - tile_height // 2))
            else:
                # Regular tiles are displayed at normal size
                scaled_tile_image = pygame.transform.scale(tile.image, (tile_width, tile_height))
                self.screen.blit(scaled_tile_image, (tile_rect.x, tile_rect.y))


    def display_game_info(self):
        info_text = [
            f"Round: {self.round_num}",
            f"Score: {self.score}",
            f"Required Score: {self.round_num * self.score_multiplier}",
            f"Play Chances: {self.play_num}",
            f"Discard Chances: {self.discard_num}",
            f"Deck: {len(self.deck)} tiles left",
            "Press 'Q' to play hand",
            "Press 'W' to discard",
        ]
        for i, text in enumerate(info_text):
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (int(self.width * 0.05), int(self.height * 0.05) + i * int(self.height * 0.05)))

    def display_buttons(self):
        play_button = pygame.Rect(self.width - int(self.width * 0.25), int(self.height * 0.05), int(self.width * 0.18), int(self.height * 0.08))
        discard_button = pygame.Rect(self.width - int(self.width * 0.25), int(self.height * 0.15), int(self.width * 0.18), int(self.height * 0.08))
        
        pygame.draw.rect(self.screen, (0, 128, 0), play_button)
        pygame.draw.rect(self.screen, (128, 0, 0), discard_button)
        
        play_text = self.font.render("Play", True, (255, 255, 255))
        discard_text = self.font.render("Discard", True, (255, 255, 255))
        
        self.screen.blit(play_text, (play_button.x + play_button.width // 4, play_button.y + play_button.height // 4))
        self.screen.blit(discard_text, (discard_button.x + discard_button.width // 8, discard_button.y + discard_button.height // 4))
        
        if self.action == 'discard':
            discard_indices_text = self.font.render(f"Selected: {self.discard_indices}", True, (0, 0, 0))
            self.screen.blit(discard_indices_text, (int(self.width * 0.05), self.height - int(self.height * 0.27)))
            confirm_discard_text = self.font.render("Press 'E' to confirm discard", True, (0, 0, 0))
            self.screen.blit(confirm_discard_text, (int(self.width * 0.05), self.height - int(self.height * 0.31)))

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
        play_button = pygame.Rect(self.width - int(self.width * 0.25), int(self.height * 0.05), int(self.width * 0.18), int(self.height * 0.08))
        discard_button = pygame.Rect(self.width - int(self.width * 0.25), int(self.height * 0.15), int(self.width * 0.18), int(self.height * 0.08))
        
        if play_button.collidepoint(mouse_pos):
            self.action = 'play'
        elif discard_button.collidepoint(mouse_pos):
            self.action = 'discard'

    def handle_tile_selection(self, mouse_pos):
        y = self.height - int(self.height * 0.1)
        x_offset = int(self.width * 0.08)
        tile_width = int(self.width * 0.05)
        tile_height = int(self.height * 0.15)
        spacing = int(tile_width * 0.2)  # Ensure this matches the spacing in display_hand

        for i, tile in enumerate(self.player.tiles):
            tile_rect = pygame.Rect(x_offset + i * (tile_width + spacing), y, tile_width, tile_height)
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
