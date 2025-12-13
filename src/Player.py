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

    def get_owner(self):
        return self.owner

    def has_any_states(self):
        return len(self.states) > 0

    def print_no_states(self):
        print(f"Owner {self.owner} -> Number of states: {len(self.states)}")

    def add_state(self, state : State):
        if state.is_state_valid():
            self.states.append(state)
        else:
            state.get_central_hex().set_central_hex_status(False)
            state = None

    def find_state_by_central(self, central_hex : Hex.Hex):
        for state in self.states:
            if state.get_central_hex() == central_hex:
                return state
        return None

    def remove_state_by_central(self, central_hex):
        for state in self.states:
            if state.get_central_hex() == central_hex:
                self.states.remove(state)
                return

    def state_includes_tile(self, tile : Hex.Hex):
        for state in self.states:
            if state.state_contains_tile(tile):
                return state
        return None

