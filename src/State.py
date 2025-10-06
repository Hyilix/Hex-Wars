from Hex import Hex
from HexMap import HexMap

class State:
    def __init__(self, owner : int, central_hex : Hex):
        self.owner = owner
        self.central_hex = central_hex

        # The hexes of the state
        self.state_hexes = [central_hex]

        # State economy
        self.income = 0
        self.money = 0

    def get_owner(self):
        return self.owner

    def set_owner(self, owner : int):
        self.owner = owner

    def get_central_hex(self):
        return self.central_hex

    def set_central_hex(self, central_hex : Hex):
        self.central_hex = central_hex

    # Get the hexes of a state starting from the central hex
    def hex_march(self):
        pass

    # TODO: class methods for splitting, merging states
    # TODO: class methods for getting the hexes of states, adding/removing hexes from states
