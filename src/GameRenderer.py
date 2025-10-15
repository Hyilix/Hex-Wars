import pygame
from pygame.transform import threshold

import Hex
import HexMap
import State
import Player

import colors
from utils import clamp

# Default texture path
DEFAULT_TEXTURE_PATH : str = "../assets/textures/"

# The default chunk size in tiles. It is intended for the first value to be even
DEFAULT_CHUNK_SIZE = (8, 8)

# The zoom values to cache chunk resize
CHUNK_ZOOM_CACHE = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

# TODO: Lazy chunk generation, generate chunks on demand and leave them in Cache
# TODO: Cache chunks at preset zoom levels, and clear cache when new zoom level entered

class Camera:
    def __init__(self, size : tuple[int, int], position : tuple[int, int], zoom : int):
        self.position : tuple[int, int] = position
        self.size = size
        # self.camera_boundaries = boundaries
        self.zoom = zoom
        self.panning_mode = False
        self.pan_pivot : tuple[int, int] = (0, 0)

    # Change the size of the camera
    def set_zoom_size(self, zoom : float):
        self.position = (int(self.position[0] * zoom // self.zoom), int(self.position[1] * zoom // self.zoom))
        self.zoom = zoom

    def set_position(self, position : tuple[int, int]):
        self.position = position

    def get_corner_position(self):
        return (self.position[0] - self.size[0] // 2, self.position[1] - self.size[1] // 2)

    # Change the camera position
    def add_direction(self, direction : tuple[int, int]):
        (x_pos, y_pos) = self.position
        self.set_position((x_pos - direction[0], y_pos - direction[1]))
        self.pan_pivot = (self.pan_pivot[0] + direction[0], self.pan_pivot[1] + direction[1])

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

class HexChunk:
    def __init__(self, tile_size : tuple[int, int], start_position : tuple[int, int]):
        self.chunk_size = DEFAULT_CHUNK_SIZE
        self.tile_size = tile_size
        self.surface_size = (tile_size[0] * self.chunk_size[0] * 3 // 4 + tile_size[0] // 4,
                             tile_size[1] * self.chunk_size[1] + tile_size[1] // 2)
        self.start_position = (start_position[0] * self.surface_size[0],
                               start_position[1] * self.surface_size[1])

        self.chunk_surface : pygame.Surface = pygame.Surface(self.surface_size, pygame.SRCALPHA)
        self.chunk_scale = 1

    # Scale surface to preferred scale
    def scale_surface(self, scale : float):
        # del self.scaled_chunk_surface
        # self.scaled_chunk_surface = pygame.transform.scale_by(self.chunk_surface, scale)

        new_size = (self.surface_size[0] * scale, self.surface_size[1] * scale)

        self.chunk_surface = pygame.transform.scale(self.chunk_surface, new_size)
        self.chunk_scale = scale

    # Scale surface to original size
    def scale_to_original(self):
        self.scale_surface(1 / self.chunk_scale)

class GameRenderer:
    def __init__(self, screen, camera : Camera, color_scheme, zoom_settings : tuple[float, float, float] = (0.2, 6, 0.1)): 
        self.chunk_size = DEFAULT_CHUNK_SIZE

        # Renderer Camera
        self.camera = camera

        # Zoom settings (min_scale, max_scale, scale_step)
        self.zoom_settings = zoom_settings

        self.screen = screen
        self.color_scheme = color_scheme
        self.texture_path = DEFAULT_TEXTURE_PATH

        # Hex Info
        self.hex_surface : pygame.Surface
        self.hex_surface_basic_size = (0, 0)
        self.hex_surface_scale = 1

        self.current_zoom = 1

        # Colored Hexes Cache
        self.hex_cache : list[HexCacheUnit] = []

        # Chunk Surfaces Map
        self.chunks : list[list[HexChunk]] = []

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

    def set_zoom(self, new_zoom : float):
        new_zoom = clamp(new_zoom, self.zoom_settings[0], self.zoom_settings[1])
        for y in range(len(self.chunks)):
            for x in range(len(self.chunks[y])):
                # self.chunks[y][x].scale_surface(new_zoom);
                pass

        self.current_zoom = new_zoom
        self.camera.set_zoom_size(new_zoom)

    # Initialise all chunks into memory
    def init_chunks(self, map_dimensions : tuple[int, int]):
        (chunks_x, chunks_y) = (map_dimensions[0] // self.chunk_size[0], map_dimensions[1] // self.chunk_size[1])

        # Check for edge chunks
        if map_dimensions[0] % self.chunk_size[0]:
            chunks_x += 1
        if map_dimensions[1] % self.chunk_size[1]:
            chunks_y += 1

        # print("chunks:", chunks_x, chunks_y)

        # Create the chunks
        for y in range(chunks_y):
            self.chunks.append([])
            for x in range(chunks_x):
                self.chunks[y].append(HexChunk(self.hex_surface_basic_size, (x, y)))

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
    def draw_tile(self, tile : Hex.Hex, new_color : tuple[int, int, int], chunk_surf : pygame.Surface):
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

        tile_x %= self.chunk_size[0]
        tile_y %= self.chunk_size[1]

        tile_offset_x = tile_x

        tile_y *= hex_size[1]
        tile_x *= hex_size[0]
        tile_x -= hex_size[0] * tile_offset_x // 4

        # Lower the hexagons on the odd positions
        if tile.position[0] % 2 == 1:
            tile_y += hex_size[1] // 2

        chunk_surf.blit(temp_hex_surface, (tile_x, tile_y))

    # Generate all the chunks from the map
    def load_chunks(self, hexmap : HexMap.HexMap):
        if not hexmap:
            return

        map_size = hexmap.dimensions
        print(map_size)

        for y in range(map_size[1]):
            for x in range(map_size[0]):
                tile = hexmap.get_hexmap()[y][x]
                color = self.color_scheme[tile.owner]
                chunk_surface = self.chunks[y // self.chunk_size[1]][x // self.chunk_size[0]].chunk_surface
                self.draw_tile(tile, color, chunk_surface)

        if not self.chunks[0][0]:
            return

        for y in range(len(self.chunks)):
            for x in range(len(self.chunks[y])):
                self.chunks[y][x].scale_surface(self.current_zoom)

    # Update a chunk from a changed tile
    def update_chunk(self, tile : Hex.Hex):
        (x_tile, y_tile) = tile.position
        chunk_surface = self.chunks[y_tile // self.chunk_size[1]][x_tile // self.chunk_size[0]].chunk_surface
        color = self.color_scheme[tile.owner]
        self.draw_tile(tile, color, chunk_surface)

    # Draw all chunks to screen
    def draw_chunks(self):
        if not self.chunks[0][0]:
            return

        chunk_size : tuple[int, int] = self.chunks[0][0].surface_size

        for y in range(len(self.chunks)):
            for x in range(len(self.chunks[y])):
                # Get the position for the next chunk
                x_chunk_pos = x * chunk_size[0] * self.current_zoom - (x * self.hex_surface_basic_size[0] * self.current_zoom // 4)
                y_chunk_pos = y * chunk_size[1] * self.current_zoom - (y * self.hex_surface_basic_size[1] * self.current_zoom // 2)

                # Apply camera offset
                x_chunk_pos -= self.camera.get_corner_position()[0]
                y_chunk_pos -= self.camera.get_corner_position()[1]

                self.screen.blit(pygame.transform.scale_by(self.chunks[y][x].chunk_surface, self.current_zoom), (x_chunk_pos, y_chunk_pos))

