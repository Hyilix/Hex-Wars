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
        if state.is_state_valid():
            self.states.append(state)
        else:
            state.get_central_hex().set_central_hex_status(False)
            state = None

    def state_includes_tile(self, hexmap : HexMap.HexMap ,tile : Hex.Hex, excluded_state : State):
        for state in self.states:
            if state.state_contains_tile(tile) and state != excluded_state:
                # Found another state. Merge with it
                state.hex_march(hexmap)
                excluded_state = None
                return

