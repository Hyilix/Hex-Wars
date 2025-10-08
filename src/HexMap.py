from Hex import Hex

class HexMap:
    def __init__(self, x_tile_count : int, y_tile_count : int):
        self.dimensions = (x_tile_count, y_tile_count)
        self.hexmap = [[]]
        self.fill_map()

    def change_map_size(self, x_count_new : int, y_count_new : int):
        self.dimensions = (x_count_new, y_count_new)

    def fill_map(self):
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                self.hexmap[y].append(Hex(x, y, -1))
            self.hexmap.append([])

    def get_hex_from_pos(self, x_pos : int, y_pos : int):
        # Out of bounds check
        if x_pos < 0 or y_pos < 0 or x_pos >= self.dimensions[0] or y_pos >= self.dimensions[1]:
            return None
        return self.hexmap[y_pos][x_pos]

    def get_hexmap(self):
        return self.hexmap

    # Returns a neighbor of input index
    def get_hex_neighbor(self, tile : Hex, index : int):
        (tile_pos_x, tile_pos_y) = tile.get_position()
        index = index % 6

        # Check if tile exists
        if tile_pos_x == None or tile_pos_y == None:
            return None

        # Check all indeces
        if index == 0:
            tile_pos_y -= 1
        elif index == 1:
            tile_pos_x += 1
        elif index == 2:
            tile_pos_x += 1
            tile_pos_y += 1
        elif index == 3:
            tile_pos_y += 1
        elif index == 4:
            tile_pos_y += 1
            tile_pos_x -= 1
        elif index == 5:
            tile_pos_x -= 1

        return self.get_hex_from_pos(tile_pos_x, tile_pos_y)

    # Returns an array containing all 6 neighbors of a hex
    def get_hex_all_neighbors(self, tile : Hex):
        neighbors = []
        for index in range(6):
            neighbors.append(self.get_hex_neighbor(tile, index))
        return neighbors

    # TODO: add unit movement (or get the hexes that a unit can move to)

# Index of each neighbour
#            _____
#           /     \
#          /       \
#    ,----(    0    )----.
#   /      \       /      \
#  /        \_____/        \
#  \    5   /     \   1    /
#   \      /       \      /
#    )----(   self  )----(
#   /      \       /      \
#  /    4   \_____/   2    \
#  \        /     \        /
#   \      /       \      /
#    `----(    3    )----'
#          \       /
#           \_____/

