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

    # Change color of the hex
    def change_color(self, new_color : tuple[int, int, int]):
        pygame.transform.threshold(
            dest_surface = self.surface,
            surface = self.surface,
            search_color = self.color,
            threshold = (0, 0, 0, 0),
            set_color = new_color,
            inverse_set = True
        )
        self.color = new_color

    # Delete this surface
    def delete_surface(self):
        del self.surface

class GameRenderer:
    def __init__(self, screen, color_scheme, zoom_settings : tuple[float, float, float] = (0.5, 4, 0.1), texture_path : str = "../assets/textures/"):
        # Zoom settings (min_scale, max_scale, scale_step)
        self.zoom_settings = zoom_settings

        self.screen = screen
        self.color_scheme = color_scheme
        self.texture_path = texture_path

        # Hex Info
        self.hex_surface : pygame.Surface
        self.hex_surface_basic_size = (0, 0)
        self.hex_surface_scale = 1

        # Colored Hexes Cache
        self.hex_cache : list[HexCacheUnit] = []

        # Background Info
        self.background_surface = pygame.Surface

    # Load new hex surface
    def load_hex_surface(self, scale : float = 1, img_name : str = "HexTile.png"):
        self.hex_surface = pygame.image.load(self.texture_path + img_name)
        self.hex_surface_basic_size = self.hex_surface.get_size()
        self.hex_surface_scale = scale

        self.clear_hex_cache()
        self.hex_cache = [HexCacheUnit(colors.shader_color, self.hex_surface)]

    # Load new background surface
    def load_background_surface(self, scale : int = 1, img_name : str = "Background.png"):
        self.background_surface = pygame.image.load(self.texture_path + img_name)

    # Search in cache
    def find_hex_by_color(self, color : tuple[int, int, int]):
        for unit in self.hex_cache:
            if unit.color == color:
                return unit.surface
        return None

    # Add new surface to cache
    def add_hex_color(self, color : tuple[int, int, int]):
        hex_unit = HexCacheUnit(colors.shader_color, self.hex_surface.copy())
        hex_unit.change_color(color)
        self.hex_cache.append(hex_unit)
        return hex_unit.surface

    # Clear the surface cache
    def clear_hex_cache(self):
        for unit in self.hex_cache:
            unit.delete_surface()
            self.hex_cache.remove(unit)
            del unit

    # Draw one tile to the screen
    def draw_tile(self, tile : Hex.Hex, new_color : tuple[int, int, int]):
        # Skip non-existing tiles
        if not tile or tile.owner == -1:
            return

        # Change the inner color of the tile
        temp_hex_surface = self.find_hex_by_color(new_color)

        # Only generate new surface when needed
        if not temp_hex_surface:
            temp_hex_surface = self.add_hex_color(new_color)

        # Render the hex on the chunk surface
        # Calculate the position of the hex before rendering
        hex_size = self.hex_surface_basic_size

        (tile_x, tile_y) = tile.position

        tile_offset_x = tile_x

        tile_y *= hex_size[1]
        tile_x *= hex_size[0]
        tile_x -= hex_size[0] * tile_offset_x // 4

        # Lower the hexagons on the odd positions
        if tile.position[0] % 2 == 1:
            tile_y += hex_size[1] // 2

        self.screen.blit(temp_hex_surface, (tile_x, tile_y))

    # Draw all chunks to screen
    def draw_tiles(self, hexmap : list[list[Hex.Hex]]):
        for y in range(len(hexmap)):
            for x in range(len(hexmap[y])):
                # Get the position for the next chunk
                tile = hexmap[y][x]
                self.draw_tile(tile, self.color_scheme[tile.owner])

