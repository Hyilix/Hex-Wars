import pygame
from pygame.transform import threshold

import Hex
import HexMap
import State
import Player

import colors

class HexCacheUnit:
    def __init__(self, color : tuple[int, int, int], surface : pygame.Surface):
        self.color = color
        self.surface = surface

class GameRenderer:
    def __init__(self, screen, color_scheme, texture_path : str = "../assets/textures/"):
        self.screen = screen
        self.color_scheme = color_scheme
        self.texture_path = texture_path

        # Basic Surfaces
        self.hex_surface : pygame.Surface
        self.hex_surface_basic_size = (0, 0)
        self.hex_surface_scale = 1

        self.background_surface = pygame.Surface
        self.background_surface_basic_size = (0, 0)
        self.background_surface_scale = 1

        # Colored Hexes Cache
        self.hex_cache = [HexCacheUnit(colors.shader_color, hex_surface)]

    def load_hex_surface(self, scale : int = 1, img_name : str = "HexTile.png"):
        self.hex_surface = pygame.image.load(self.texture_path + img_name)
        self.hex_surface_basic_size = self.hex_surface.get_size()
        self.hex_surface = pygame.transform.scale_by(self.hex_surface, scale)

        self.hex_surface_scale = scale

        self.clear_hex_cache()
        self.hex_cache = [(colors.shader_color, self.hex_surface)]

    def scale_hex_surface(self, scale : int):

    def load_background_surface(self, scale : int = 1, img_name : str = "Background.png"):
        self.background_surface = pygame.image.load(self.texture_path + img_name)
        self.background_surface_basic_size = self.background_surface.get_size()
        self.background_surface = pygame.transform.scale_by(self.background_surface, scale)

        self.background_surface_scale = scale

    # Search in cache
    def find_hex_by_color(self, color : tuple[int, int, int]):
        for surf in self.hex_cache:
            if surf[0] == color:
                return surf[1]

        return None

    # Add new surface to cache
    def add_hex_color(self, color : tuple[int, int, int], surf):
        self.hex_cache.append((color, surf))

    # Clear the surface cache
    def clear_hex_cache(self):
        for item in self.hex_cache:
            if not item[0] == colors.shader_color:
                # Clear surface from memory
                surf = item[1]
                del surf

                # Remove element from list
                self.hex_cache.pop(1)

    # Draw one tile to the screen
    def draw_tile(self, tile : Hex.Hex, new_color : tuple[int, int, int]):
        # Skip non-existing tiles
        if not tile or tile.owner == -1:
            # print(tile.owner)
            return

        # Change the inner color of the tile
        old_color = colors.shader_color
        temp_hex_surface = self.find_hex_by_color(new_color)

        # Only generate new surface when needed
        if not temp_hex_surface:
            temp_hex_surface = self.hex_surface.copy()

            pygame.transform.threshold(
                dest_surface = temp_hex_surface,
                surface = self.hex_surface,
                search_color = old_color,
                threshold = (0, 0, 0, 0),
                set_color = new_color,
                inverse_set = True
            )
            self.add_hex_color(new_color, temp_hex_surface)

        # Render the hex on the screen
        # Calculate the position of the hex before rendering
        hex_size = self.hex_surface_basic_size
        hex_scale = self.hex_surface_scale

        (tile_x, tile_y) = tile.position
        tile_y *= hex_size[1] * hex_scale
        tile_x *= hex_size[0] * hex_scale
        tile_x -= hex_size[0] * hex_scale * tile.position[0] // 4

        # Lower the hexagons on the odd positions
        if tile.position[0] % 2 == 1:
            tile_y += hex_size[1] * hex_scale // 2

        self.screen.blit(temp_hex_surface, (tile_x, tile_y))

    # Draw the entire map
    def draw_map(self, hexmap : HexMap.HexMap):
        if not hexmap:
            return

        map_size = hexmap.dimensions

        for y in range(map_size[1]):
            for x in range(map_size[0]):
                tile = hexmap.get_hexmap()[y][x]
                color = self.color_scheme[tile.owner]
                self.draw_tile(tile, color)

