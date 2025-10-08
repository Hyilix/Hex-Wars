from Doodads import Doodad

def reverse_neighbor_index(index : int):
    index = index % 6
    return (index + 3) % 6

class Hex:
    def __init__(self, x_pos : int, y_pos : int, owner = -1):
        self.position = (x_pos, y_pos)
        self.owner = owner

        # An array representing the rivers
        self.rivers = [False] * 6

        # The doodad contained inside the Hex
        self.doodad = None

        # The hex that will contain the town center (the central hex of a state)
        self.is_central_hex = False

    def get_position(self):
        return self.position

    def set_position(self, new_x : int, new_y : int):
        self.position = (new_x, new_y)

    def set_river(self, index : int, is_river : bool):
        self.rivers[index % 6] = is_river

    def get_rivers(self):
        return self.rivers

    def get_river_index(self, index : int):
        return self.rivers[index % 6]

    def set_owner(self, owner : int):
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_doodad(self, doodad : Doodad):
        self.doodad = doodad

    def get_doodad(self):
        return self.doodad

    def set_central_hex_status(self, is_central : bool):
        self.is_central_hex = is_central

    def get_central_hex_status(self):
        return self.is_central_hex

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

