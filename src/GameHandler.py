import pygame

import GameRenderer
import Editor
import HexMap
import Menu

import colors

import KeyboardState

from enum import Enum

class CurrentTab(Enum):
    MAINMENU = 1
    LOBBY = 2
    MAPPICKER = 3
    EDITOR = 4
    GAMEPLAY = 5

# Singleton class for handling the game with its different menus and functions
class GameHandler:
    __instance = None
    __initialized = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not GameHandler.__initialized:
            self.__current_tab = None

            self.__renderer : GameRenderer.GameRenderer = None
            self.__editor : Editor.Editor = None
            self.__menu = None

            self.__camera : GameRenderer.Camera = None
            self.__hex_map : HexMap.HexMap = None

            self.__screen : pygame.Surface = None
            self.__color_scheme : list[tuple[int, int, int]] = None

            GameHandler.__initialized = True

    def __is_editor_set_up(self):
        return self.__screen and self.__editor and self.__hex_map and self.__camera

    def set_color_scheme(self, scheme : list[tuple[int, int, int]]):
        self.__color_scheme = scheme

    # It is expected that the set_screen method will be called after initializing the handler
    def set_screen(self, screen):
        self.__screen = screen

    def create_default_hexmap(self):
        self.__hex_map = HexMap.HexMap(20, 20, 0)

    def create_default_renderer(self):
        self.__renderer = GameRenderer.GameRenderer(self.__screen, self.__camera, self.__color_scheme)
        self.__renderer.load_hex_surface("HexTile.png", 1)
        self.__renderer.init_chunks(self.__hex_map.dimensions)
        self.__renderer.get_visible_chunks()
        self.__renderer.load_chunks(self.__hex_map)

    def create_default_editor(self):
        self.__editor = Editor.Editor(self.__renderer, self.__hex_map, self.__screen.get_size())

    def create_default_camera(self):
        self.__camera = GameRenderer.Camera(self.__screen.get_size(), (0, 0), 1)

    def clear_everything(self):
        self.__hex_map = None
        self.__color_scheme = None
        self.__editor = None
        self.__renderer = None
        self.__menu = None
        self.__camera = None

    def switch_tab(self, next_menu):
        self.__current_tab = next_menu
        self.clear_everything()
        self.handle_tabs()

    def pan_camera(self, new_coord : tuple[int, int]):
        if self.__editor == None or not self.__editor.is_blocked():
            # Pan the camera
            if self.__camera.panning_mode == True:
                (x_dir, y_dir) = (new_coord[0] - self.__camera.pan_pivot[0], new_coord[1] - self.__camera.pan_pivot[1])
                self.__camera.add_direction((x_dir, y_dir))
                self.__renderer.get_visible_chunks()

    def set_camera_pan_pivot(self, mouse_pos : tuple[int, int]):
        self.__camera.pan_pivot = pygame.mouse.get_pos()

    def set_camera_panning_mode(self, mode : bool):
        self.__camera.panning_mode = mode

    def set_camera_zoom(self, val):
        self.__renderer.set_zoom(round(val, 1) * self.__renderer.zoom_settings[2] + self.__renderer.current_zoom)

    def editor_handle_mouse_action(self, mouse_pos, click_once = False):
        if not self.__is_editor_set_up():
            return

        tile_pos = self.__camera.get_tile_at_position(mouse_pos)
        # Check if tile is within bounds
        if (tile_pos[0] >= 0 and tile_pos[0] < self.__hex_map.dimensions[0] and
            tile_pos[1] >= 0 and tile_pos[1] < self.__hex_map.dimensions[1]):
            current_tile = self.__hex_map.get_tile_at_position(tile_pos)
            self.__editor.handle_mouse_action(mouse_pos, current_tile, click_once)
        elif click_once == True:
            self.__editor.handle_mouse_action(mouse_pos, None, click_once)

    def editor_handle_keyboard(self):
        self.__editor.handle_keyboard_action(self.__screen)

    def draw_renderer_chunks(self):
        self.__renderer.draw_chunks()

    def draw_editor_tabs(self):
        self.__editor.render_tabs(self.__screen)

    def draw_every_frame(self):
        if self.__renderer:
            self.draw_renderer_chunks()

        if self.__editor and self.__renderer:
            self.draw_editor_tabs()

    def set_new_map_editor(self):
        self.__hex_map = self.__editor.get_editor_map()

    def center_camera(self):
        self.__camera.set_position(self.__renderer.get_map_center(self.__hex_map))
        self.__renderer.get_visible_chunks()

    def handle_tabs(self):
        if self.__current_tab == CurrentTab.MAINMENU:
            pass

        elif self.__current_tab == CurrentTab.EDITOR:
            print("Current Tab -> EDITOR")
            color_scheme = [colors.gray_dark, colors.red, colors.blue, colors.green, colors.yellow, colors.purple, colors.cyan, colors.pink]
            self.set_color_scheme(color_scheme)
            self.create_default_camera()
            self.create_default_hexmap()
            self.create_default_renderer()
            self.create_default_editor()

        elif self.__current_tab == CurrentTab.GAMEPLAY:
            pass

        elif self.__current_tab == CurrentTab.LOBBY:
            pass

        elif self.__current_tab == CurrentTab.MAPPICKER:
            pass

