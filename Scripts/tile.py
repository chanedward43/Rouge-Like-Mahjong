class Tile:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = str(value)  # Ensure value is always a string

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __repr__(self):
        return f"{self.value}{self.suit}"