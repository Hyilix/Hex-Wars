import pygame

import Doodads
import HexMap
import Hex
import State
import Player
import GameRenderer
import MapHandling
import Collisions_2d
import button
import colors

# Tab super class for all the editor's tabs
class Tab:
    def __init__(self, position : tuple[int, int], size : tuple[int, int]):
        self.__pos = position
        self.__size = size

        self.__is_clicked_inside = False
        self.__buttons : list[button.Button] = []

    # Get is_clicked_inside state
    def get_clicked_inside(self):
        return self.__is_clicked_inside

    # Clear is_clicked_inside state
    def clear_clicked_inside(self):
        self.__is_clicked_inside = False

    # Determine if the mouse is inside the tab
    def click_action(self, mouse_pos : tuple[int, int]):
        self.__is_clicked_inside = Collisions_2d.point_rect(mouse_pos, self.__pos, self.__size)
        return self.__is_clicked_inside

    # Get the buttons into the internal buttons list.
    # Buttons' positions don't matter, as they will be set by spread_buttons method
    def fill_buttons_list(self, buttons : list[button.Button]):
        self.__buttons = buttons.copy()

    # Spread the buttons evenly on the tab, having equal distance between them on the x-axis
    def spread_buttons(self, buttons_per_row : int):
        no_buttons = len(self.__buttons)
        button_distance = (self.__size[0] // buttons_per_row, 10)

        # Set button position
        for button in self.__buttons:
            for x in range(buttons_per_row):
                pass

# The main editor class
class Editor:
    def __init__(self, renderer : GameRenderer.GameRenderer, hex_map : HexMap.HexMap):
        self.__renderer = renderer
        self.__hex_map = hex_map

        self.__map_name = "New Map"
        self.__players = []
        self.__current_player = 0

        self.__config = {
                "Hash": 0,
                "Name": self.__map_name,
                "Players": self.__players,
                "CurrentPlayer": self.__current_player,
                "Map": self.__hex_map
                }

    # Load a game and save the game configuration
    def load_game(self, game_name : str):
        config = MapHandling.load_game(game_name)
        self.__config = config
        self.__renderer.reload_renderer(self.__hex_map)

    # Save the current game
    def save_game(self, game_name : str):
        MapHandling.save_game(self.__config, game_name)


