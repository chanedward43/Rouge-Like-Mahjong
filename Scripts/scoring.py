from collections import Counter

class Scoring:
    def __init__(self, hand):
        self.hand = hand.tiles.copy()  # Use a copy to avoid modifying the original hand
        self.triplets = []
        self.sequences = []
        self.doubles = []

    def calculate_score(self):
        self.find_triplets()
        self.find_sequences()
        self.find_doubles()

        total_value = 0
        total_multiplier = 0
        highest_double = 0

        for triplet in self.triplets:
            if triplet[0].suit == 'special':
                total_value += 11 * 3
            else:
                total_value += 3 * int(triplet[0].value)
            total_multiplier += 3

        for sequence in self.sequences:
            total_value += sum(int(tile.value) for tile in sequence if tile.value.isdigit())
            total_multiplier += 3

        if not self.doubles:
            pass
        else:
            double_len = len(self.doubles) - 1
            if self.doubles[double_len][0].suit == 'special':
                total_value += 11 * 2
            else:
                total_value += 2 * int(self.doubles[double_len][0].value)
            total_multiplier += 2

        for double in self.doubles:
            if double[0].suit == 'special':
                 highest_double = 11
                 break
            elif int(double[0].value) > highest_double:
                highest_double = int(double[0].value)

        if highest_double == 0:
            pass
        else:
            total_value += highest_double * 2
            total_multiplier += 2

        if total_multiplier == 0:
            return 0  # To avoid division by zero

        print(f"Triplets: {self.triplets}")
        print(f"Sequences: {self.sequences}")
        print(f"Doubles: {self.doubles}")
        print(f"Total value: {total_value}")
        print(f"Total multiplier: {total_multiplier}")
        return total_value * total_multiplier

    def find_triplets(self):
        counter = Counter((tile.suit, tile.value) for tile in self.hand)
        for (suit, value), count in counter.items():
            if count >= 3 and value != 'special':
                triplet = [tile for tile in self.hand if tile.suit == suit and tile.value == value][:3]
                self.triplets.append(triplet)
                self.remove_tiles(triplet)
            elif count >= 3 and value == 'special':
                triplet = [tile for tile in self.hand if tile.suit == suit and tile.value == value][:3]
                self.triplets.append(triplet)
                self.remove_tiles(triplet)

    def find_sequences(self):
        filtered_hand = [tile for tile in self.hand if tile.value.isdigit()]
        sorted_hand = sorted(filtered_hand, key=lambda x: (x.suit, int(x.value)))
        for i in range(len(sorted_hand) - 2):
            if (sorted_hand[i].suit == sorted_hand[i + 1].suit == sorted_hand[i + 2].suit and
                    int(sorted_hand[i].value) + 1 == int(sorted_hand[i + 1].value) and
                    int(sorted_hand[i].value) + 2 == int(sorted_hand[i + 2].value)):
                sequence = sorted_hand[i:i + 3]
                self.sequences.append(sequence)
                self.remove_tiles(sequence)

    def find_doubles(self):
        counter = Counter((tile.suit, tile.value) for tile in self.hand)
        for (suit, value), count in counter.items():
            if count == 2 and value != 'special':
                double = [tile for tile in self.hand if tile.suit == suit and tile.value == value][:2]
                self.doubles.append(double)
                self.remove_tiles(double)
            elif count == 2 and value == 'special':
                double = [tile for tile in self.hand if tile.suit == suit and tile.value == value][:2]
                self.doubles.append(double)
                self.remove_tiles(double)

    def remove_tiles(self, tiles_to_remove):
        for tile in tiles_to_remove:
            if tile in self.hand:
                self.hand.remove(tile)
