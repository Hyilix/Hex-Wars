from Hex import Hex

empty_hex = Hex(0, 0, -1)

class HexMap:
    def __init__(self, x_tile_count : int, y_tile_count : int):
        self.dimensions = (x_tile_count, y_tile_count)
        self.hexmap = [[empty_hex] * x_tile_count] * y_tile_count

    def get_hex_from_pos(self, x_pos : int, y_pos : int):
        return self.hexmap[y_pos][x_pos]

