import State
import Hex
import Doodads
import HexMap

class Player:
    def __init__(self, owner):
        self.owner = owner
        self.states = [None]
