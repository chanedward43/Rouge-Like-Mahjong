import pygame

class Tile:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = str(value)
        self.image = self.load_image()

    def load_image(self):
        image_path = f"assets/tiles/{self.suit}_{self.value}.png"
        return pygame.image.load(image_path)

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __repr__(self):
        return f"{self.value}{self.suit}"