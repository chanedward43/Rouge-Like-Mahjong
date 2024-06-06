class Hand:
    def __init__(self):
        self.tiles = []

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.sort_tiles()

    def remove_tile(self, tile):
        self.tiles.remove(tile)
        self.sort_tiles()

    def sort_tiles(self):
        order = {'bam': 0, 'cir': 1, 'cha': 2, 'special': 3}
        special_order = {'east': 0, 'south': 1, 'west': 2, 'north': 3, 'white': 4, 'green': 5, 'red': 6}
        self.tiles.sort(key=lambda x: (order[x.suit], int(x.value) if x.value.isdigit() else special_order[x.value]))

    def __repr__(self):
        return ' '.join(str(tile) for tile in self.tiles)
