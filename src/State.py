from Hex import Hex
from HexMap import HexMap

class State:
    def __init__(self, owner : int, central_hex : Hex):
        self.owner = owner
        self.central_hex = central_hex

    def get_owner(self):
        return self.owner

    def set_owner(self, owner : int):
        self.owner = owner

    def get_central_hex(self):
        return self.central_hex

    def set_central_hex(self, central_hex : Hex):
        self.central_hex = central_hex

