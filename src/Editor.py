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
import Events

import ActionHandler
import KeyboardState
import InfoTabs
import ButtonHandler

# Enum class for representing current tab opened
class TabMenu(Enum):
    WORLD = 10

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

    def get_buttons(self):
        return self.__buttons

    def buttons_click_action(self, mouse_pos : tuple[int, int], editor):
        for button in self.__buttons:
            if button.check_mouse_collision(mouse_pos):
                button.call_function(editor, button)

    # Determine if the mouse is inside the tab
    def click_action(self, mouse_pos : tuple[int, int]):
        self.__is_clicked_inside = Collisions_2d.point_rect(mouse_pos, self.__pos, self.__size)
        return self.__is_clicked_inside

    # Get the buttons into the internal buttons list.
    # Buttons' positions don't matter, as they will be set by spread_buttons method
    def fill_buttons_list(self, buttons : list[button.Button]):
        self.__buttons = buttons.copy()

    def add_buttons(self, buttons : list[button.Button]):
        last_pos = self.__buttons[-1].get_pos()

        last_y = last_pos[1] + 2 * buttons[0].get_size()[1]
        print(f"Last y pos: {last_y}")

        for button in buttons:
            button.change_pos((self.__size[0] // 2 - button.get_size()[0] // 2, last_y))
            last_y += button.get_size()[1] + 10
            self.__buttons.append(button)

    # Spread the buttons evenly on the tab, having equal distance between them on the x-axis
    def spread_buttons(self, buttons_per_row : int = 0):
        y_offset = 10
        x_offset = 10

        if buttons_per_row == 0:
            # Calculate how many buttons can fit with proper spacing
            button_width = self.__buttons[0].get_size()[0]
            available_width = self.__size[0] - (2 * x_offset)

            # Estimate spacing (use a minimum spacing value)
            min_spacing = 10
            buttons_per_row = max(1, available_width // (button_width + min_spacing))

        # Calculate spacing between buttons
        available_width = self.__size[0] - (2 * x_offset)
        button_width = self.__buttons[0].get_size()[0]

        # Calculate spacing to distribute buttons evenly
        total_button_width = button_width * buttons_per_row
        remaining_space = available_width - total_button_width
        spacing = remaining_space // (buttons_per_row + 1)

        # Set button positions
        row = 0
        col = 0
        for button in self.__buttons:
            x_pos = self.__pos[0] + x_offset + spacing + col * (button_width + spacing)
            y_pos = self.__pos[1] + y_offset + row * (button.get_size()[1] + y_offset)
            button.change_pos((x_pos, y_pos))

            # Move to next column, or wrap to next row
            col += 1
            if col == buttons_per_row:
                col = 0
                row += 1

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

    def draw_tab(self, screen):
        self.draw_background_color(screen)
        for button in self.__buttons:
            button.draw(screen)

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

    def apply_brush(self, hex_map : HexMap.HexMap, start_hex : Hex.Hex, tile_list : list[Hex.Hex]):
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
                tile_list.append(tile)

            # Set new doodad
            if self.__owner >= 0:
                if tile.doodad == None or self.__doodad == None or tile.doodad.get_name() != self.__doodad.get_name():
                    if tile.doodad != self.__doodad:
                        action_list.add_action(ActionHandler.Action(ActionHandler.ActionType.TILE, copy.deepcopy(tile.doodad), copy.deepcopy(self.__doodad), 'doodad', tile))
                        if tile not in tile_list:
                            tile_list.append(tile)

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

        # The map size, written in string
        self.__map_size = str(hex_map.dimensions[0]) + "x" + str(hex_map.dimensions[1])

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
        self.__is_blocked = False

        self.action_handler = ActionHandler.History()
        self.__current_action_list = None

        self.brush = Brush(1, False, -1, None)

        self.__active_tab = TabMenu.WORLD

        self.worldtab = Tab((3 * screen_size[0] // 4, 0), ((screen_size[0] // 4, screen_size[1])), colors.tab_color)
        self.worldtab.fill_buttons_list(ButtonHandler.load_world_buttons())
        self.worldtab.spread_buttons()

        self.utiltab = Tab((0, 0), (screen_size[0] // 4, screen_size[1]), colors.tab_color)
        self.utiltab.fill_buttons_list(ButtonHandler.load_main_buttons())
        self.utiltab.spread_buttons()
        self.utiltab.add_buttons(ButtonHandler.load_misc_buttons())

        self.help_info = InfoTabs.InfoHelp((screen_size[0] // 12, screen_size[1] // 12))
        self.save_info = InfoTabs.InfoSave((screen_size[0] // 12, screen_size[1] // 12))
        self.load_info = InfoTabs.InfoLoad((screen_size[0] // 12, screen_size[1] // 12))
        self.map_info = InfoTabs.InfoMap((screen_size[0] // 12, screen_size[1] // 12))

    def is_blocked(self):
        return self.__is_blocked

    # Convert from string to pair of ints
    def __map_size_from_str(self, map_size : str):
        if map_size.count('x') == 1:
            width, height = map(int, map_size.split('x'))
            return (int(width), int(height))
        else:
            print("Invalid map size format")
            return None

    def __map_size_to_str(self, map_size : tuple[int, int]):
        return str(map_size[0]) + 'x' + str(map_size[1])

    def change_map_dimensions(self):
        new_dims = self.__map_size_from_str(self.__map_size)

        if new_dims == None:
            return

        print("Changing map dimension")

        del self.__hex_map

        self.__hex_map = HexMap.HexMap(new_dims[0], new_dims[1], 0)
        self.__renderer.reload_renderer(self.__hex_map)
        self.__config["Map"] = self.__hex_map

        pygame.event.post(pygame.event.Event(Events.MAP_CHANGED))

    # Load a game and save the game configuration
    def load_game(self):
        game_name = self.__config.get("Name")
        config = MapHandling.load_map(game_name)
        if config != None:
            self.__config = config

            self.__hex_map = self.__config.get("Map")
            self.__renderer.reload_renderer(self.__hex_map)
            self.__map_size = self.__map_size_to_str(self.__hex_map.dimensions)

            pygame.event.post(pygame.event.Event(Events.MAP_CHANGED))

    def get_editor_map(self):
        return self.__hex_map

    # Save the current game
    def save_game(self):
        MapHandling.save_map(self.__config, self.__renderer)

    def change_owner(self, new_owner):
        self.brush.change_owner(new_owner)

    def change_doodad(self, new_doodad):
        self.brush.change_doodad(new_doodad)

    def set_fill(self, fill : bool):
        self.brush.change_fill(fill)

    def apply_brush(self, start_hex : Hex.Hex):
        tile_list : list[Hex.Hex] = []
        action_list = self.brush.apply_brush(self.__hex_map, start_hex, tile_list)

        self.action_handler.add_action_list(action_list)

        self.__renderer.update_list_chunks(tile_list)
        tile_list = []

    def make_new_action_list(self):
        self.__current_action_list = ActionHandler.ActionList([])

    def set_action_list(self):
        if self.__current_action_list:
            self.action_handler.add_action_list(self.__current_action_list)
        self.__current_action_list = None

    def render_tabs(self, screen):
        if self.__tabs_visible:
            if self.__active_tab == TabMenu.WORLD:
                self.worldtab.draw_tab(screen)

            self.utiltab.draw_tab(screen)

        self.help_info.render(screen)
        self.save_info.render_with_name(screen, self.__config.get("Name"))
        self.load_info.render_with_name(screen, self.__config.get("Name"))
        self.map_info.render_with_name(screen, self.__map_size)

    def handle_mouse_action(self, mouse_pos : tuple[int, int], tile, click_once = False):
        if self.__is_blocked:
            return

        first_collision = self.utiltab.click_action(mouse_pos)
        second_collision = self.worldtab.click_action(mouse_pos)

        if (first_collision or second_collision) and self.__tabs_visible:
            self.__map_focus = False
        else:
            self.__map_focus = True

        if self.__map_focus == True and tile != None:
            self.apply_brush(tile)
        elif click_once == True and self.__tabs_visible:
            if first_collision:
                self.utiltab.buttons_click_action(mouse_pos, self)
            elif second_collision:
                self.worldtab.buttons_click_action(mouse_pos, self)

        self.utiltab.clear_clicked_inside()
        self.worldtab.clear_clicked_inside()

    def handle_keyboard_action(self, screen):
        keyboardstate = KeyboardState.KeyboardState()
        key_pressed = keyboardstate.key_pressed
        key_down = keyboardstate.key_is_down

        # Close any info tab open
        if key_pressed == pygame.K_ESCAPE:
            if self.help_info.to_render():
                self.help_info.toggle_render()
            if self.save_info.to_render():
                self.save_info.toggle_render()
            if self.load_info.to_render():
                self.load_info.toggle_render()
            if self.map_info.to_render():
                self.map_info.toggle_render()
                self.__map_size = self.__map_size_to_str(self.__hex_map.dimensions)

            self.__is_blocked = False

        # Save/Load when tab is open
        if key_pressed == pygame.K_RETURN:
            if self.save_info.to_render():
                self.save_game()
                self.save_info.toggle_render()
            if self.load_info.to_render():
                self.load_game()
                self.load_info.toggle_render()
            if self.map_info.to_render():
                self.change_map_dimensions()
                self.map_info.toggle_render()

            self.__is_blocked = False

        if keyboardstate.is_ctrl_hold:
            if key_down == True:
                # Action handler
                if self.__is_blocked == False:
                    if key_pressed == pygame.K_z:
                        self.handle_action_handler(True)
                    elif key_pressed == pygame.K_y:
                        self.handle_action_handler(False)

                    # Tab handler
                    if key_pressed == pygame.K_v:
                        self.__switch_tab_visility()

                if key_pressed == pygame.K_h:
                    if not self.save_info.to_render() and not self.load_info.to_render() and not self.map_info.to_render():
                        self.help_info.toggle_render()
                        self.__is_blocked = self.help_info.to_render()

                if key_pressed == pygame.K_l:
                    if not self.help_info.to_render() and not self.save_info.to_render() and not self.map_info.to_render():
                        self.load_info.toggle_render()
                        self.__is_blocked = self.load_info.to_render()

                if key_pressed == pygame.K_m:
                    if not self.help_info.to_render() and not self.save_info.to_render() and not self.load_info.to_render():
                        self.map_info.toggle_render()
                        self.__is_blocked = self.map_info.to_render()

                if key_pressed == pygame.K_s and keyboardstate.is_shift_hold == False:
                    if not self.help_info.to_render() and not self.load_info.to_render() and not self.map_info.to_render():
                        self.save_info.toggle_render()
                        self.__is_blocked = self.save_info.to_render()

                if key_pressed == pygame.K_s and keyboardstate.is_shift_hold == True:
                    self.save_game()
        else:
            if self.save_info.to_render():
                if keyboardstate.unicode != None and keyboardstate.key_pressed != None and keyboardstate.key_is_down == True:
                    new_name = self.save_info.add_key(keyboardstate.unicode, keyboardstate.key_pressed, self.__config.get("Name"))

                    if new_name != None:
                        self.__config["Name"] = new_name

            if self.load_info.to_render():
                if keyboardstate.unicode != None and keyboardstate.key_pressed != None and keyboardstate.key_is_down == True:
                    new_name = self.load_info.add_key(keyboardstate.unicode, keyboardstate.key_pressed, self.__config.get("Name"))

                    if new_name != None:
                        self.__config["Name"] = new_name

            if self.map_info.to_render():
                if keyboardstate.unicode != None and keyboardstate.key_pressed != None and keyboardstate.key_is_down == True:
                    new_size = self.map_info.add_key(keyboardstate.unicode, keyboardstate.key_pressed, self.__map_size)

                    if new_size != None:
                        self.__map_size = new_size

    def handle_action_handler(self, to_undo : bool):
        if to_undo:
            self.action_handler.undo_last_action()
        else:
            self.action_handler.redo_last_action()
        self.__renderer.load_chunks(self.__hex_map)

    # Local functions
    def __switch_tab_visility(self):
        self.__tabs_visible = not self.__tabs_visible

