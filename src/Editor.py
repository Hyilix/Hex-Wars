import pygame
from enum import Enum

import copy

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
import KeyboardState
import InfoTabs

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

        screen.blit(self.__color_surface, self.__pos)

class Brush:
    def __init__(self, size : int, fill : bool, owner : int, doodad : Doodads.Doodad):
        self.__size = size
        self.__fill = fill
        self.__owner = owner
        self.__doodad = doodad

    def change_size(self, size : int):
        self.__size = size

    def change_fill(self, fill : bool):
        self.__fill = fill

    def change_owner(self, owner : int):
        self.__owner = owner

    def change_doodad(self, doodad : Doodads.Doodad):
        self.__doodad = doodad

    def apply_brush(self, hex_map : HexMap.HexMap, start_hex : Hex.Hex):
        # Get all the tiles that need to be modified
        action_list = ActionHandler.ActionList([])
        if self.__fill == True:
            tiles = hex_map.get_identical_neighboring_hexes(start_hex)
        else:
            tiles = hex_map.get_neighbors_at_level(start_hex, self.__size)

        for tile in tiles:
            # Set new owner
            if tile.owner != self.__owner:
                action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE, tile.owner, self.__owner, 'owner', tile))

            # Set new doodad
            if self.__owner >= 0:
                if tile.doodad == None or tile.doodad.get_name() != self.__doodad.get_name():
                    action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE, copy.deepcopy(tile.doodad), copy.deepcopy(self.__doodad), 'doodad', tile))

        return action_list

# The main editor class
class Editor:
    def __init__(self, renderer : GameRenderer.GameRenderer, hex_map : HexMap.HexMap, screen_size : tuple[int, int]):
        self.__renderer : GameRenderer.GameRenderer = renderer
        self.__hex_map = hex_map

        self.__map_name = "New Map"
        self.__players = []
        self.__current_player = 0

        self.__screen_size = screen_size

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
        self.__tabs_visible = True

        self.action_handler = ActionHandler.History()

        self.brush = Brush(2, False, 3, Doodads.Tree())

        self.__active_tab = TabMenu.WORLD

        self.worldtab = Tab((3 * screen_size[0] // 4, 0), ((screen_size[0] // 4, screen_size[1])), colors.tab_color)
        self.utiltab = Tab((0, 0), (screen_size[0] // 4, screen_size[1]), colors.tab_color)

        self.test_info = InfoTabs.InfoTab(False, 4.0, (screen_size[0] // 12, 11 * screen_size[1] // 12))

    # Load a game and save the game configuration
    def load_game(self, game_name : str):
        config = MapHandling.load_game(game_name)
        self.__config = config
        self.__renderer.reload_renderer(self.__hex_map)

    # Save the current game
    def save_game(self, game_name : str):
        MapHandling.save_game(self.__config, game_name)

    def apply_brush(self, start_hex : Hex.Hex):
        print("Editor applied brush")
        action_list = self.brush.apply_brush(self.__hex_map, start_hex)

        self.action_handler.add_action_list(action_list)

        self.__renderer.load_chunks(self.__hex_map)

    def render_tabs(self, screen):
        if self.__tabs_visible:
            if self.__active_tab == TabMenu.WORLD:
                self.worldtab.draw_background_color(screen)

            self.utiltab.draw_background_color(screen)

    def handle_mouse_action(self, mouse_pos : tuple[int, int], tile):
        first_collision = self.utiltab.click_action(mouse_pos)
        second_collision = self.worldtab.click_action(mouse_pos)

        if (first_collision or second_collision) and self.__tabs_visible:
            self.__map_focus = False
        else:
            self.__map_focus = True

        if self.__map_focus == True:
            self.apply_brush(tile)

        self.utiltab.clear_clicked_inside()
        self.worldtab.clear_clicked_inside()

    def handle_keyboard_action(self, screen):
        keyboardstate = KeyboardState.KeyboardState()

        if keyboardstate.is_ctrl_hold:
            key_pressed = keyboardstate.key_pressed
            key_down = keyboardstate.key_is_down

            if key_down == True:
                # Action handler
                if key_pressed == pygame.K_z:
                    self.__handle_action_handler(True)
                elif key_pressed == pygame.K_y:
                    self.__handle_action_handler(False)

                # Tab handler
                if key_pressed == pygame.K_v:
                    self.__switch_tab_visility()

                if key_pressed == pygame.K_h:
                    self.test_info.render_text("Hello", screen)

    # Local functions
    def __handle_action_handler(self, to_undo : bool):
        if to_undo:
            self.action_handler.undo_action_last()
        else:
            self.action_handler.redo_last_action()
        self.__renderer.load_chunks(self.__hex_map)

    def __switch_tab_visility(self):
        self.__tabs_visible = not self.__tabs_visible

