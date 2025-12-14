from collections import deque

from Hex import Hex
from HexMap import HexMap
import Doodads

class State:
    def __init__(self, owner : int, central_hex : Hex):
        self.owner = owner
        self.central_hex = central_hex
        central_hex.set_central_hex_status(True)

        # The hexes of the state
        self.state_hexes = [central_hex]

        # State economy
        self.income = 0
        self.money = 10

        # If money ever reaches negative, this will be set to True
        # If this is True, all the units of the state will be deleted
        self.is_bankrupt = False

    def get_income(self):
        return self.income

    def get_money(self):
        return self.money

    def get_owner(self):
        return self.owner

    def set_owner(self, owner : int):
        self.owner = owner

    def get_central_hex(self):
        return self.central_hex

    def get_state_hexes(self):
        return self.state_hexes

    def set_central_hex(self, central_hex : Hex):
        if central_hex in self.state_hexes:
            self.central_hex.set_central_hex_status(False)
            self.central_hex = central_hex
            self.central_hex.set_central_hex_status(True)

    def find_new_central_hex(self):
        # Find the first empty tile
        for i in range(len(self.state_hexes)):
            if not self.state_hexes[i].doodad:
                self.central_hex = self.state_hexes[i]
                self.state_hexes[i].set_central_hex_status(True)
                return self.central_hex

        # If all tiles are occupied, force the first one to be central
        self.central_hex = self.state_hexes[0]
        self.state_hexes[0].set_central_hex_status(True)
        return self.central_hex

    # Determine if a hex is inside an estate
    def is_hex_in_state(self, tile : Hex):
        return tile in self.state_hexes

    # Update the income of the state
    def update_income(self):
        self.income = 0
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

    def set_state_hexes(self, hexes):
        self.state_hexes = hexes[:]

    # Get the hexes of a state starting from the central hex
    def hex_march(self, hexmap : HexMap):
        hexqueue = deque()
        hexqueue.append(self.central_hex)
        visited = [self.central_hex]

        other_central_hexes = []

        # Search all the hexes for a state
        while hexqueue:
            current = hexqueue.popleft()
            neighbors = hexmap.get_hex_all_neighbors(current)
            for tile in neighbors:
                if tile and tile.get_owner() == self.owner and tile not in visited:
                    hexqueue.append(tile)
                    visited.append(tile)
                    # print("Found new tile in hex march")
                    if tile.get_central_hex_status() and tile != self.central_hex:
                        other_central_hexes.append(tile)

        # Copy the visited hexes onto the state_hexes
        self.state_hexes = visited[:]

        return other_central_hexes

    # Search only for tiles in the included_tiles
    def restrained_hex_march(self, hexmap : HexMap, included_tiles : list[Hex]):
        hexqueue = deque()
        hexqueue.append(self.central_hex)
        visited = [self.central_hex]

        other_central_hexes = []

        # Search all the hexes for a state
        while hexqueue:
            current = hexqueue.popleft()
            neighbors = hexmap.get_hex_all_neighbors(current)
            for tile in neighbors:
                if tile and tile.get_owner() == self.owner and tile not in visited and tile in included_tiles:
                    hexqueue.append(tile)
                    visited.append(tile)
                    # print(f"Found new tile in hex march, {tile.get_position()}")
                    if tile.get_central_hex_status() and tile != self.central_hex:
                        other_central_hexes.append(tile)

        # Copy the visited hexes onto the state_hexes
        self.state_hexes = visited[:]

        # if len(other_central_hexes):
        #     self.central_hex.set_central_hex_status(False)
        #     self.central_hex = other_central_hexes[0]
        #     self.central_hex.set_central_hex_status(True)

    # Add a hex to the state_hexes
    def add_hex(self, tile : Hex):
        self.state_hexes.append(tile)

    # Remove a hex from the state_hexes
    def remove_hex(self, tile : Hex):
        self.state_hexes.remove(tile)
        if not self.is_state_valid():
            print("We are an invalid state")

    def state_contains_tile(self, tile : Hex):
        return tile in self.state_hexes

    def is_state_valid(self):
        state_valid = len(self.state_hexes) > 1
        return state_valid

    def ready_all_units(self):
        for tile in self.get_state_hexes():
            if isinstance(tile.doodad, Doodads.Unit):
                tile.doodad.set_can_action(True)
                print(f"Tile found to set action -> {tile.get_position()}")

    def unready_all_units(self):
        for tile in self.get_state_hexes():
            if isinstance(tile.doodad, Doodads.Unit):
                tile.doodad.set_can_action(False)

    def split_state(self, hexmap : HexMap, states):
        former_state = self.state_hexes[:]

        self.hex_march(hexmap)

        for tile in self.state_hexes:
            if tile in former_state:
                if tile.get_central_hex_status() and tile != self.central_hex:
                    self.central_hex.set_central_hex_status(False)
                    self.central_hex = tile
                    self.central_hex.set_central_hex_status(True)
                former_state.remove(tile)

        print(f"Number of hexes left: {len(former_state)}")

        # If there are any tiles left, create and split the states
        if len(former_state) >= 1:
            former_state[0].set_central_hex_status(True)
            new_state = State(self.owner, former_state[0])
            new_state.set_state_hexes(former_state)

            states.append(new_state)

            new_state.split_state(hexmap, states)

