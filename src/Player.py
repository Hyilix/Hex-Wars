from State import State
import Hex
import Doodads
import HexMap

class Player:
    def __init__(self, owner : int, color : tuple[int, int, int], name : str = "Player"):
        self.owner = owner
        self.color = color
        self.name = name

        self.states = []

    def change_name(self, new_name : str):
        self.name = new_name

    def change_color(self, new_color : tuple[int, int, int]):
        self.color = new_color

    def get_states(self):
        return self.states

    def add_state(self, state : State):
        self.states.append(state)

