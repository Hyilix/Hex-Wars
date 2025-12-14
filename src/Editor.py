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
import utils

import ActionHandler
import KeyboardState
import InfoTabs
import ButtonHandler
from Tabs import Tab
from Tabs import TabMenu

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
                    if tile.doodad != self.__doodad and (tile.doodad == None or tile.doodad.get_name() != "Base"):
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
        self.__players = [None, None, None, None, None, None]
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

        pygame.event.post(pygame.event.Event(Events.CENTER_CAMERA))

    def is_blocked(self):
        return self.__is_blocked

    # Change map dimension and fire event to change hexmap
    def change_map_dimensions(self):
        new_dims = utils.map_size_from_str(self.__map_size)

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
            self.__map_size = utils.map_size_to_str(self.__hex_map.dimensions)

            self.__players = self.__config.get("Players")

            for row in self.__hex_map.hexmap:
                for tile in row:
                    if tile.doodad:
                        tile.doodad.set_can_action(False)

            self.action_handler.deep_clear()
            self.__renderer.reload_renderer(self.__hex_map)

            pygame.event.post(pygame.event.Event(Events.MAP_CHANGED))

    # Save the current game
    def save_game(self):
        MapHandling.save_map(self.__config, self.__renderer)

    def get_hex_map(self):
        return self.__hex_map

    def get_players(self):
        return self.__players

    def get_renderer(self):
        return self.__renderer

    # Change the owner used for the brush
    def change_owner(self, new_owner):
        self.brush.change_owner(new_owner)

    # Change the doodad used for the brush
    def change_doodad(self, new_doodad):
        self.brush.change_doodad(new_doodad)

    # Change the fill used for the brush
    def set_fill(self, fill : bool):
        self.brush.change_fill(fill)

    # Apply brush to the map
    def apply_brush(self, start_hex : Hex.Hex):
        tile_list : list[Hex.Hex] = []
        action_list = self.brush.apply_brush(self.__hex_map, start_hex, tile_list)

        self.action_handler.add_action_list(action_list)

        # Make new action list to put the towncenter and the player
        state_action_list = ActionHandler.ActionList([])

        modified_tiles = []

        if len(tile_list) > 0:
            modified_tiles = utils.state_handling(self, tile_list, state_action_list)

        self.action_handler.extend_last_list(state_action_list)

        if modified_tiles:
            tile_list.extend(modified_tiles)

        self.__renderer.update_list_chunks(tile_list)
        tile_list = []


    def make_new_action_list(self):
        self.__current_action_list = ActionHandler.ActionList([])

    def set_action_list(self):
        if self.__current_action_list:
            self.action_handler.add_action_list(self.__current_action_list)
        self.__current_action_list = None

    # Render everything
    def render_tabs(self, screen):
        if self.__tabs_visible:
            if self.__active_tab == TabMenu.WORLD:
                self.worldtab.draw_tab(screen)

            self.utiltab.draw_tab(screen)

        self.help_info.render(screen)
        self.save_info.render_with_name(screen, self.__config.get("Name"))
        self.load_info.render_with_name(screen, self.__config.get("Name"))
        self.map_info.render_with_name(screen, self.__map_size)

    # Handle the mouse input
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

    # Handle the keyboard input
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
                self.__map_size = utils.map_size_to_str(self.__hex_map.dimensions)

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

    # Local functions
    def __switch_tab_visility(self):
        self.__tabs_visible = not self.__tabs_visible

