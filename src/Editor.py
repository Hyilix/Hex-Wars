import pygame
from enum import Enum

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

import ActionHandler

# Enum class for representing current tab opened
class TabMenu(Enum):
    WORLD = 10
    ECONOMY = 11
    SETTINS = 12

# Tab super class for all the editor's tabs
class Tab:
    def __init__(self, position : tuple[int, int], size : tuple[int, int], background_color : tuple[int, int, int, int]):
        self.__pos = position
        self.__size = size

        self.__is_clicked_inside = False
        self.__buttons : list[button.Button] = []
        self.__background_color = background_color

        self.__color_surface : pygame.Surface
        self.create_color_surface()

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
        y_offset = 10
        button_distance = (self.__buttons[0].__size[0] // buttons_per_row, y_offset)

        y_size = self.__buttons[0].__size[1] + y_offset

        # Set button position
        x = 0
        for button in self.__buttons:
            button.change_pos((x * button_distance[0], (button.__size[1] % y_size) * y_size))

            # Increment x
            x += 1
            if x == buttons_per_row:
                x = 0

    def change_background_color(self, new_color : tuple[int, int, int, int]):
        self.__background_color = new_color

    # Create the background color surface
    def create_color_surface(self):
        self.__color_surface = pygame.Surface(self.__size, pygame.SRCALPHA)
        self.__color_surface.fill(self.__background_color)

    # Draw the tab background to the screen
    def draw_background_color(self, screen):
        if not self.__background_color:
            self.create_color_surface()

        screen.blit(self.__background_color, self.__pos)

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

        # True -> action is focused on the Map
        # False -> action is focused on the tabs
        self.__map_focus = True

    # Load a game and save the game configuration
    def load_game(self, game_name : str):
        config = MapHandling.load_game(game_name)
        self.__config = config
        self.__renderer.reload_renderer(self.__hex_map)

    # Save the current game
    def save_game(self, game_name : str):
        MapHandling.save_game(self.__config, game_name)


