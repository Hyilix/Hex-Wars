from collections import deque

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

        # If money ever reaches negative, this will be set to True
        # If this is True, all the units of the state will be deleted
        self.is_bankrupt = False

    def get_owner(self):
        return self.owner

    def set_owner(self, owner : int):
        self.owner = owner

    def get_central_hex(self):
        return self.central_hex

    def set_central_hex(self, central_hex : Hex):
        self.central_hex = central_hex

    # Determine if a hex is inside an estate
    def is_hex_in_estate(self, tile : Hex):
        return tile in self.state_hexes

    # Update the income of the state
    def update_income(self):
        for tile in self.state_hexes:
            self.income += tile.income
            if (tile.doodad):
                self.income += tile.doodad.income

    # Add/Subtract money based on state income
    def add_income(self):
        self.money += self.income
        if self.money < 0:
            self.is_bankrupt = True
            self.money = 0

    # Get the hexes of a state starting from the central hex
    def hex_march(self, hexmap : HexMap):
        hexqueue = deque()
        hexqueue.append(self.central_hex)

        visited = [self.central_hex]

        # Search all the hexes for a state
        while hexqueue[0]:
            neighbors = hexmap.get_hex_all_neighbors(hexqueue[0])
            for tile in neighbors:
                if tile.get_owner() == self.owner and tile not in visited:
                    hexqueue.append(tile)
                    visited.append(tile)

            hexqueue.popleft()

        # Copy the visited hexes onto the state_hexes
        self.state_hexes = visited[:]

    # Add a hex to the state_hexes
    def add_hex(self, tile : Hex):
        self.state_hexes.append(tile)
        # TODO: check new hex neighbors and merge the states

    # Remove a hex from the state_hexes
    def remove_hex(self, tile : Hex):
        self.state_hexes.remove(tile)

    # TODO: class methods for splitting, merging states
    # TODO: class methods for getting the hexes of states, adding/removing hexes from states

