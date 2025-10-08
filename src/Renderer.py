import pygame

import Hex
import HexMap

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

class MapRenderer(Renderer):
    def __init__(self, textures_path : str):
        super().__init__(textures_path)

