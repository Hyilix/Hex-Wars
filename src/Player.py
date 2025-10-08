from State import State
import Hex
import Doodads
import HexMap

class Player:
    def __init__(self, owner):
        self.owner = owner

        self.states = []

    def get_states(self):
        return self.states

    def add_state(self, state : State):
        self.states.append(state)

