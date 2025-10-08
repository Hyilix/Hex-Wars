import pygame

import Hex
import HexMap

# TODO:
# The method of creating a big surface for the map is inneficient
# Look for other alternatives

# General Renderer
class Renderer:
    def __init__(self, textures_path : str, font_path : str = ""):
        self.textures_path = textures_path
        self.font_path = font_path

        self.screen = None
        self.fonts = []

    def change_textures_path(self, path_to_dir : str):
        self.textures_path = path_to_dir

    def change_font_path(self, path_to_dir : str):
        self.font_path = path_to_dir

    def setup_screen(self, screen_size : tuple[int, int], flags = 0, display_name : str = "Hex Game"):
        # Ensure display module initialization
        if not pygame.display.get_init():
            pygame.display.init()

        pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption(display_name)

    def load_image_surface(self, path_to_image : str):
        return pygame.image.load(self.textures_path + path_to_image)

# Renderer for the hexmap
class MapRenderer(Renderer):
    def __init__(self, textures_path : str):
        super().__init__(textures_path)
        self.map_surface = None
        self.tile_surface = self.load_image_surface("HexMap.png")

    # Create a new surface for the map
    def create_surface(self, dimensions : tuple[int, int]):
        self.map_surface = pygame.Surface(dimensions)

    def add_tile(self, position = tuple[int, int]):
        pass

