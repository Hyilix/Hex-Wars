import copy

import Doodads
import Hex
import Player
import State
import ActionHandler

# Clamp function
def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    return n

# Helper function to check for any state including the tile
def __check_state_interuption(self, tile : Hex.Hex, action_list, modified_tiles, states_checked):
    # Find the player that held the tile before
    for player in self.get_players():
        if not player:
            continue

        if player.get_owner() == tile.owner:
            continue

        # Find a state that has the tile
        state = player.state_includes_tile(tile)
        if state:
            state.remove_hex(tile)

            if not state.is_state_valid():
                print("Preemptly removed invalid state")
                child_tile = state.get_central_hex()

                if action_list:
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            copy.deepcopy(child_tile.doodad), None,
                                            'doodad', child_tile))

                player.remove_state_by_central(child_tile)

                if action_list:
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            child_tile.get_central_hex_status(), False,
                                            'is_central_hex', child_tile))

                modified_tiles.append(child_tile)

                # Check if player has any states
                if not player.has_any_states():
                    print(f"Remove player {player.get_owner()}")
                    self.get_players()[player.get_owner() - 1] = None
                    player = None

                continue

            # Central tile has been removed, select another one
            if tile.get_central_hex_status():
                new_central = state.find_new_central_hex()

                if action_list:
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            copy.deepcopy(tile.doodad), None,
                                            'doodad', tile))
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            copy.deepcopy(new_central.doodad), copy.deepcopy(Doodads.TownCenter(new_central.owner)),
                                            'doodad', new_central))

                modified_tiles.append(tile)
                modified_tiles.append(new_central)

            if state not in states_checked:
                states_checked.append(state)

# Helper function to search checked states for invalid states
def __search_checked_states(self, checked_state, action_list, modified_tiles):
    checked_state_tile = checked_state.get_central_hex()

    child_states = []
    checked_state.split_state(self.get_hex_map(), child_states)

    print(f"Number of child states: {len(child_states)}")
    if not checked_state.is_state_valid():
        print("Handle an invalid state")

        if action_list:
            action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                    copy.deepcopy(checked_state_tile.doodad), None,
                                    'doodad', checked_state_tile))

        self.get_players()[checked_state.get_owner() - 1].remove_state_by_central(checked_state_tile)
        if action_list:
            action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                    checked_state_tile.get_central_hex_status(), False,
                                    'is_central_hex', checked_state_tile))
        modified_tiles.append(checked_state_tile)

    for child_state in child_states:
        child_tile = child_state.get_central_hex()

        if not child_state.is_state_valid():
            print("Handle an invalid state")

            if action_list:
                action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                        copy.deepcopy(child_tile.doodad), None,
                                        'doodad', child_tile))

            self.get_players()[child_state.get_owner() - 1].remove_state_by_central(child_tile)
            if action_list:
                action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                        child_tile.get_central_hex_status(), False,
                                        'is_central_hex', child_tile))
            modified_tiles.append(child_tile)
            continue

        if action_list:
            action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                    copy.deepcopy(child_tile.doodad), copy.deepcopy(Doodads.TownCenter(child_tile.owner)),
                                    'doodad', child_tile))

        modified_tiles.append(child_tile)

        self.get_players()[child_state.get_owner() - 1].add_state(child_state)

# Build the states that are being drawn
def state_handling(self, tile_list : list[Hex.Hex], action_list):
    modified_tiles = []

    # Check if a state is being iterrupted
    states_checked = []
    for tile in tile_list:
        __check_state_interuption(self, tile, action_list, modified_tiles, states_checked)

    # Search in checked states for any invalid states
    for checked_state in states_checked:
        __search_checked_states(self, checked_state, action_list, modified_tiles)

    # Debug for printing the number of states for each player
    for player in self.get_players():
        if player:
            player.print_no_states()

    # If owner is of a player, handle the states
    tile_list_copy = tile_list[:]
    for tile in tile_list_copy:
        # print("Handle new tile")
        owner = tile.owner
        if owner > 0:
            new_state = State.State(owner, tile)

            new_state.restrained_hex_march(self.get_hex_map(), tile_list)

            for new_tile in new_state.get_state_hexes():
                if new_tile in tile_list_copy:
                    tile_list_copy.remove(new_tile)

            # Player found
            if self.get_players()[owner - 1] != None:
                old_central = new_state.get_central_hex()

                # Check if there are any other states around
                neighbors = []
                self.get_hex_map().get_neighbors_around_clump(tile_list, neighbors)

                for neighbor in neighbors:
                    other_state = self.get_players()[owner - 1].state_includes_tile(neighbor)

                    if other_state:
                        if action_list:
                            action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                                    old_central.get_central_hex_status(), False,
                                                    'is_central_hex', old_central))
                        other_centers = other_state.hex_march(self.get_hex_map())

                        # Remove the merged states
                        for old_tile in other_centers:
                            print(f"Old Tile pos : {old_tile.get_position()}")
                            if action_list and old_tile.doodad and old_tile.doodad.get_name() == "Base":
                                action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            copy.deepcopy(old_tile.doodad), None,
                                            'doodad', old_tile))

                            modified_tiles.append(old_tile)

                            self.get_players()[owner - 1].remove_state_by_central(old_tile)

                        new_state = None
                        return modified_tiles

                # If no other state found, search the contents of this state
                new_state.hex_march(self.get_hex_map())

                # Check if there can be a state
                if not new_state.is_state_valid():
                    new_central_hex = new_state.get_central_hex()
                    if action_list:
                        action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                                new_central_hex.get_central_hex_status(), False,
                                                'is_central_hex', new_central_hex))
                    modified_tiles.append(new_state.get_central_hex())
                    new_state = None
                    continue

                new_central = new_state.get_central_hex()

                if action_list:
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            copy.deepcopy(new_central.doodad), copy.deepcopy(Doodads.TownCenter(owner)),
                                            'doodad', new_central))

                modified_tiles.append(new_central)

                self.get_players()[owner - 1].add_state(new_state)

            else:
                # No player found, create one
                new_state.hex_march(self.get_hex_map())

                # Check if there can be a state
                if not new_state.is_state_valid():
                    new_central_hex = new_state.get_central_hex()
                    if action_list:
                        action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                                new_central_hex.get_central_hex_status(), False,
                                                'is_central_hex', new_central_hex))
                    modified_tiles.append(new_state.get_central_hex())
                    new_state = None
                    continue

                print("We have new player")
                new_player = Player.Player(owner, self.get_renderer().get_color_scheme()[owner])
                new_player.add_state(new_state)

                central_tile = new_state.get_central_hex()
                if action_list:
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE,
                                            copy.deepcopy(tile.doodad), copy.deepcopy(Doodads.TownCenter(owner)),
                                            'doodad', central_tile))
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.PLAYER,
                                            None, new_player,
                                            owner - 1, self.get_players()))

                modified_tiles.append(central_tile)

    return modified_tiles
