import pygame
import copy

import GameRenderer
import Hex
import HexMap
import Player
import Doodads

import button
import utils
import Events
import colors

import MapHandling

import ActionHandler
import KeyboardState
import ButtonHandler

from Tabs import Tab
from Tabs import TabMenu

# The gameplay class that handler the gameplay aspects of the game
class Gameplay:
    def __init__(self, renderer : GameRenderer.GameRenderer, hex_map : HexMap.HexMap, screen_size : tuple[int, int]):
        self.__renderer = renderer
        self.__hex_map = hex_map

        self.__screen_size = screen_size

        self.__players = [None, None, None, None, None, None]
        self.__current_player = 0

        self.__config = {
                "Hash": 0,
                "Name": "",
                "Players": self.__players,
                "CurrentPlayer": self.__current_player,
                "Map": self.__hex_map
                }

        self.action_handler = ActionHandler.History()

        self.__selected_tile : Hex.Hex = None

        self.__tabs_visible = False

        self.buytab = Tab((0, screen_size[1] * 4 // 5), (screen_size[0], screen_size[1] // 5), colors.tab_color)
        self.buytab.fill_buttons_list(ButtonHandler.load_buy_buttons())
        self.buytab.spread_buttons_horizontally()

        self.__building_mode = False

    def render_tabs(self, screen):
        if self.__tabs_visible:
            self.buytab.draw_tab(screen)

    # Load a game and save the game configuration
    def load_game(self, game_name):
        config = MapHandling.load_map(game_name)
        if config != None:
            self.__config = config

            self.__hex_map = self.__config.get("Map")
            for row in self.__hex_map.hexmap:
                for tile in row:
                    if tile.doodad:
                        tile.doodad.set_can_action(False)

            self.__renderer.reload_renderer(self.__hex_map)

            self.__players = self.__config.get("Players")

            self.action_handler.deep_clear()

            pygame.event.post(pygame.event.Event(Events.MAP_CHANGED))

            for row in self.__hex_map.hexmap:
                for tile in row:
                    if tile.doodad:
                        print(f"{tile.doodad.get_name()} at pos {tile.get_position()}")

    def get_players(self):
        return self.__players

    def get_hex_map(self):
        return self.__hex_map

    def get_renderer(self):
        return self.__renderer

    def is_of_current_player(self, tile : Hex.Hex):
        return tile.owner - 1 == self.__current_player

    def get_current_player(self):
        return self.__players[self.__current_player]

    # Start the current turn
    def start_current_turn(self):
        player = self.get_current_player()

        if not player:
            return

        player.print_no_states()
        player.ready_all_units()

    # End the current turn and go onto the next player
    def end_current_turn(self):
        player = self.get_current_player()

        if not player:
            return

        player.unready_all_units()

        # Prepare next player
        self.__current_player += 1
        if (not self.get_current_player()):
            self.__current_player = 0

        self.start_current_turn()

    # Handle the mouse input
    def handle_mouse_action(self, mouse_pos : tuple[int, int], tile, click_once = False):
        # Select the tile
        if not click_once:
            return

        if not tile:
            return

        # Handle the selected tile
        if not self.__selected_tile:
            if self.is_of_current_player(tile):
                if isinstance(tile.doodad, Doodads.Unit) and tile.doodad.get_can_action():
                    self.__tabs_visible = False
                    self.__selected_tile = tile

                    movable_tiles = self.__hex_map.get_movable_tiles(tile, tile.doodad.get_move_range())
                    movable_tiles.append(tile)
                    self.__renderer.set_highlighted_hexes(movable_tiles)
                elif not self.__building_mode:
                    self.__building_mode = True
                    self.__tabs_visible = not self.__tabs_visible
                    player = self.get_current_player()
                    state = player.state_includes_tile(tile)
                    self.__renderer.set_highlighted_hexes(state.get_state_hexes())
                else:
                    self.__building_mode = False
                    self.__renderer.set_highlighted_hexes()
                    self.__tabs_visible = False
            else:
                self.__building_mode = False
                self.__renderer.set_highlighted_hexes()
                self.__tabs_visible = False
            return

        print("Handle gameplay mouse")

        # Handle the movement of the unit
        action_list = ActionHandler.ActionList([])
        moved_unit = self.__hex_map.move_unit(self.__selected_tile, tile, action_list)

        if moved_unit:
            self.action_handler.add_action_list(action_list)

            state_action_list = ActionHandler.ActionList([])

            modified_tiles = []
            tile_list = [self.__selected_tile, tile]

            if len(tile_list) > 0:
                modified_tiles = utils.state_handling(self, tile_list, state_action_list)

            self.action_handler.extend_last_list(state_action_list)

            if modified_tiles:
                tile_list.extend(modified_tiles)

            self.__renderer.update_list_chunks(tile_list)
        self.__selected_tile = None
        self.__renderer.set_highlighted_hexes()

    # Handle the keyboard input
    def handle_keyboard_action(self, screen):
        keyboardstate = KeyboardState.KeyboardState()
        key_pressed = keyboardstate.key_pressed
        key_down = keyboardstate.key_is_down

        if keyboardstate.is_ctrl_hold:
            if key_down == True:
                # Action handler
                if key_pressed == pygame.K_z:
                    self.handle_action_handler(True)
                elif key_pressed == pygame.K_y:
                    self.handle_action_handler(False)

    # Handle the action handler
    def handle_action_handler(self, to_undo : bool):
        actions = []
        if to_undo:
            actions = self.action_handler.undo_last_action()
        else:
            actions = self.action_handler.redo_last_action()
        self.__renderer.set_highlighted_hexes()
        self.__selected_tile = None

        if actions:
            utils.state_handling(self, actions, None)

        self.__renderer.load_chunks(self.__hex_map)

