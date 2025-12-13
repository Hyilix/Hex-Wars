import pygame
import copy

import GameRenderer
import Hex
import HexMap
import Player

import button
import utils
import Events

import MapHandling

import ActionHandler
import KeyboardState
import ButtonHandler

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

    # Load a game and save the game configuration
    def load_game(self, game_name):
        config = MapHandling.load_map(game_name)
        if config != None:
            self.__config = config

            self.__hex_map = self.__config.get("Map")
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

    # Handle the mouse input
    def handle_mouse_action(self, mouse_pos : tuple[int, int], tile, click_once = False):
        # Select the tile
        if not click_once:
            return

        if not self.__selected_tile:
            if tile.doodad:
                self.__selected_tile = tile
            return

        print("Handle gameplay mouse")

        action_list = ActionHandler.ActionList([])
        self.__hex_map.move_unit(self.__selected_tile, tile, action_list)
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

        if actions:
            utils.state_handling(self, actions, None)

        self.__renderer.load_chunks(self.__hex_map)

