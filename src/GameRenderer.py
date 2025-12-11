import pygame
from pygame.transform import threshold
import math

import Hex
import HexMap
import State
import Player
import Collisions_2d

import colors
from utils import clamp

# Default texture path
DEFAULT_TEXTURE_PATH : str = "../assets/textures/"

# The default chunk size in tiles. It is intended for the first value to be even
DEFAULT_CHUNK_SIZE = (8, 8)

# The zoom values to cache chunk resize
CHUNK_ZOOM_CACHE = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0, 1.5, 2.0]

class Camera:
    def __init__(self, size : tuple[int, int], position : tuple[int, int], zoom : int):
        self.position : tuple[int, int] = position
        self.size = size
        self.zoom = zoom
        self.panning_mode = False
        self.pan_pivot : tuple[int, int] = (0, 0)

        self.tile_size_ref : tuple[int, int] = (0, 0)

    def set_tile_size_ref(self, new_ref : tuple[int, int]):
        self.tile_size_ref = new_ref

    # Change the size of the camera
    def set_zoom_size(self, zoom : float):
        if zoom in CHUNK_ZOOM_CACHE:
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

    # Get a tile position from camera position
    def get_tile_at_position(self, camera_position : tuple[int, int]):
        # Get world position
        (x_world, y_world) = (camera_position[0] + self.get_corner_position()[0], camera_position[1] + self.get_corner_position()[1])

        (x_tile_ref, y_tile_ref) = (self.tile_size_ref[0] * self.zoom, self.tile_size_ref[1] * self.zoom)

        (x_tile, y_tile) = (x_world // int(x_tile_ref * 3 / 2), y_world // int(y_tile_ref))
        (x_mod, y_mod) = (x_world % int(x_tile_ref * 3 / 2), y_world % int(y_tile_ref))

        # TODO: Simplify the code for more clean code

        x_tile *= 2
        y_mod //= int(y_tile_ref // 2)
        if y_mod == 0:
            y_mod = -1

        if x_mod <= int(x_tile_ref // 4):
            # Check for accurate point at the border of 2 tiles
            (x_corner_1, y_corner_1) = (x_world // int(x_tile_ref * 3 / 4), y_world // int(y_tile_ref))
            (x_corner_1, y_corner_1) = (x_corner_1 * int(x_tile_ref * 3 / 4), y_corner_1 * int(y_tile_ref) + int(y_tile_ref // 2) + (y_mod - 1) * int(y_tile_ref // 2))
            (x_corner_2, y_corner_2) = (x_corner_1 + int(x_tile_ref // 4), y_corner_1 - int(y_tile_ref // 2) + abs(y_mod) * int(y_tile_ref // 2))

            even_trig = [(x_corner_1, y_corner_1), (x_corner_1, y_corner_1 + int(y_tile_ref)), (x_corner_2, y_corner_2 + abs(y_mod) * int(y_tile_ref // 2))]
            odd_trig = [(x_corner_1, y_corner_1 - (y_mod - 1) * int(y_tile_ref // 2)), (x_corner_2, y_corner_2 - (y_mod + 1) * int(y_tile_ref // 4) - (y_mod - 1) * int(y_tile_ref // 4)), (x_corner_2, y_corner_2 + int(y_tile_ref // 2) - (y_mod - 1) * int(y_tile_ref // 4))]

            trig_collision_even = Collisions_2d.point_trig((x_world, y_world), even_trig)
            trig_collision_odd = Collisions_2d.point_trig((x_world, y_world), odd_trig)

            if trig_collision_even:
                x_tile -= 1
                # y_mod switches sign when on x odd position (lower y position)
                y_tile += (y_mod - 1) // 2

        if x_mod > int(x_tile_ref):
            # Tile placement changes slightly when x is odd
            x_tile += 1
            y_tile = (y_world - int(y_tile_ref // 2)) // int(y_tile_ref)

        elif x_mod >= int(x_tile_ref * 3 / 4) and x_mod <= int(x_tile_ref):
            # Check for accurate point at the border of 2 tiles
            (x_corner_1, y_corner_1) = (x_world // int(x_tile_ref * 3 / 4), y_world // int(y_tile_ref))
            (x_corner_1, y_corner_1) = (x_corner_1 * int(x_tile_ref * 3 / 4), y_corner_1 * int(y_tile_ref))
            (x_corner_2, y_corner_2) = (x_corner_1 + int(x_tile_ref / 4), y_corner_1 + y_mod * int(y_tile_ref // 2))

            even_trig = [(x_corner_1, y_corner_1), (x_corner_1, y_corner_1 + int(y_tile_ref)), (x_corner_2, y_corner_2 - (y_mod - 1) * int(y_tile_ref // 2))]
            odd_trig = [(x_corner_1, y_corner_1 + (y_mod + 1) * int(y_tile_ref // 2)), (x_corner_2, y_corner_2), (x_corner_2, y_corner_2 + int(y_tile_ref))]

            trig_collision_even = Collisions_2d.point_trig((x_world, y_world), even_trig)
            trig_collision_odd = Collisions_2d.point_trig((x_world, y_world), odd_trig)

            if trig_collision_odd:
                x_tile += 1
                # y_mod switches sign when on x odd position (lower y position)
                y_tile += (y_mod - 1) // 2

        return (x_tile, y_tile)

class CacheUnit:
    def __init__(self, surface : pygame.Surface):
        self.surface = surface

    # Delete the surface
    def delete_surface(self):
        del self.surface

class HexCacheUnit(CacheUnit):
    def __init__(self, color : tuple[int, int, int], surface : pygame.Surface):
        super().__init__(surface)
        self.color = color

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

class DoodadCacheUnit(CacheUnit):
    def __init__(self, surface : pygame.Surface, doodad_type : str):
        super().__init__(surface)
        self.doodad_type = doodad_type

class HexChunk:
    def __init__(self, tile_size : tuple[int, int], start_position : tuple[int, int]):
        self.chunk_size = DEFAULT_CHUNK_SIZE
        self.tile_size = tile_size
        self.surface_size : tuple[int, int] = (tile_size[0] * self.chunk_size[0] * 3 // 4 + tile_size[0] // 4,
                                                tile_size[1] * self.chunk_size[1] + tile_size[1] // 2)
        self.start_position = (start_position[0] * self.surface_size[0],
                               start_position[1] * self.surface_size[1])
        self.start_raw_position = start_position

        self.chunk_surface = None #= pygame.Surface(self.surface_size, pygame.SRCALPHA)
        self.chunk_scale = 1

    # Scale surface to preferred scale
    def scale_surface(self, scale : float):
        scale = round(scale, 1)
        # print(scale)
        if scale in CHUNK_ZOOM_CACHE:
            new_size = (self.surface_size[0] * scale, self.surface_size[1] * scale)

            # self.chunk_surface = pygame.transform.scale(self.chunk_surface, new_size)
            # self.chunk_scale = scale

    # Scale surface to original size
    def scale_to_original(self):
        self.scale_surface(1 / self.chunk_scale)

class GameRenderer:
    def __init__(self, screen, camera : Camera, color_scheme, zoom_settings : tuple[float, float, float] = (0.5, 2, 0.5)): 
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
        self.cached_zoom = self.current_zoom

        # Colored Hexes Cache
        self.hex_cache : list[HexCacheUnit] = []
        self.doodad_cache : list[DoodadCacheUnit] = []

        # Chunk Surfaces Map
        self.chunks : list[list[HexChunk]] = []

        # Background Info
        self.background_surface = None

        # Background color
        self.background_color = colors.gray_very_dark

        self.hexmap = None
        self.visible_chunks = [[]]

    # Reload the renderer when loading a new map
    def reload_renderer(self, map_obj : HexMap.HexMap):
        if not map_obj:
            # print("No map object, cannot reload renderer")
            return

        self.del_chunks()
        self.current_zoom = 1
        self.cached_zoom = 1

        self.init_chunks(map_obj.dimensions)
        self.get_visible_chunks()
        self.load_chunks(map_obj)

    # Load new hex surface
    def load_hex_surface(self, img_name : str = "HexTile.png", scale : float = 1):
        self.hex_surface = pygame.image.load(self.texture_path + img_name)
        self.hex_surface_basic_size = self.hex_surface.get_size()
        self.hex_surface_scale = scale

        self.clear_hex_cache()
        # Add a scaled surface to the cache
        scaled_hex = pygame.transform.scale_by(self.hex_surface, scale)
        self.hex_cache = [HexCacheUnit(colors.shader_color, scaled_hex)]

        self.camera.set_tile_size_ref(self.hex_surface_basic_size)

    # Load new doodad surface
    def load_doodad_surface(self, img_name : str, doodad_type : str, scale : float = 1):
        doodad_surface = pygame.image.load(self.texture_path + doodad_type + "s/" + img_name + ".png")

        self.doodad_cache.append(DoodadCacheUnit(doodad_surface, img_name))

    def change_background_color(self, color : tuple[int, int, int]):
        self.background_color = color

    # Load new background surface
    def load_background_surface(self, scale : int = 1, img_name : str = "Background.png"):
        self.background_surface = pygame.image.load(self.texture_path + img_name)
        self.background_surface = pygame.transform.scale_by(self.background_surface, scale)

    # Set the camera zoom
    def set_zoom(self, new_zoom : float):
        new_zoom = round(new_zoom, 1)
        new_zoom = clamp(new_zoom, self.zoom_settings[0], self.zoom_settings[1])
        self.current_zoom = new_zoom

        # print(f"New zoom = {new_zoom}")

        if new_zoom in CHUNK_ZOOM_CACHE:
            # print("Poof, new zoom chunks")
            self.cached_zoom = new_zoom

            # Clear doodad cache
            self.clear_doodad_cache()

            self.camera.set_zoom_size(new_zoom)
            # Clear previous chunk cache and create new one
            self.clear_visible_chunks()
            self.get_visible_chunks()

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

    def del_chunks(self):
        for row in self.chunks:
            for chunk in row:
                del chunk

        self.chunks = []

    # Search in cache
    def find_hex_by_color(self, color : tuple[int, int, int]):
        for unit in self.hex_cache:
            if unit.color == color:
                return unit.surface
        return None

    def find_doodad_by_name(self, doodad_type : str):
        for doodad in self.doodad_cache:
            if doodad.doodad_type == doodad_type:
                return doodad.surface
        return None

    # Add new surface to cache
    def add_hex_color(self, color : tuple[int, int, int]):
        hex_unit = HexCacheUnit(colors.shader_color, self.hex_surface.copy())
        hex_unit.change_color(color)
        self.hex_cache.append(hex_unit)
        return hex_unit.surface

    # Clear the hex surface cache
    def clear_hex_cache(self):
        for unit in self.hex_cache:
            unit.delete_surface()
            self.hex_cache.remove(unit)
            del unit

    # Clear the doodad surface cache
    def clear_doodad_cache(self):
        for doodad in self.doodad_cache:
            doodad.delete_surface()
            self.doodad_cache.remove(doodad)
            del doodad

    # Get the length of the hex cache. Useful for determining player count
    def get_hex_cache_count(self):
        return len(self.hex_cache)

    def get_color_scheme(self):
        return self.color_scheme

    def get_map_center(self, hexmap : HexMap.HexMap):
        map_size = (int(hexmap.dimensions[0] // 2 * (self.hex_surface_basic_size[0] * 3 // 2 * self.cached_zoom)
                    + self.hex_surface_basic_size[0] * self.cached_zoom // 4),
                    int(hexmap.dimensions[1] * self.hex_surface_basic_size[1] * self.cached_zoom
                        + self.hex_surface_basic_size[1] * self.cached_zoom // 2))

        return (map_size[0] // 2, map_size[1] // 2)

    def draw_entire_map_separate(self, hex_map : HexMap.HexMap):
        tile_size = (64, 64)

        map_size = (hex_map.dimensions[0] // 2 * (tile_size[0] * 3 // 2) + tile_size[0],
                    hex_map.dimensions[1] * tile_size[1] + tile_size[1] // 2)

        map_surf = pygame.Surface(map_size, pygame.SRCALPHA)

        # Custom draw tile function used only for this method
        def __draw_tile(self, tile : Hex.Hex, map_surf : pygame.Surface):
            # Skip non-existing tiles
            if not tile:
                return

            # Change the inner color of the tile
            temp_hex_surface = self.find_hex_by_color(self.color_scheme[tile.owner])

            # Only generate new surface when needed
            if not temp_hex_surface:
                temp_hex_surface = self.add_hex_color(self.color_scheme[tile.owner])

            temp_hex_surface = pygame.transform.scale_by(temp_hex_surface, 1)

            # Draw the lack of tile
            if tile.owner == -1:
                temp_hex_surface = temp_hex_surface.copy()
                # If a background is loaded, use that
                if self.background_surface:
                    temp_hex_surface.blit(self.background_surface, (0, 0), area=None, special_flags=pygame.BLEND_RGBA_MULT)
                # No background loaded, use the color
                else:
                    temp_hex_surface.fill((255,255,255,0), special_flags=pygame.BLEND_RGBA_ADD)
                    temp_hex_surface.fill(self.background_color, special_flags=pygame.BLEND_RGBA_MULT)

            else:
                # Load tile doodad surface
                temp_doodad_surface = None
                doodad = tile.get_doodad()
                if doodad:
                    temp_doodad_surface = self.find_doodad_by_name(doodad.get_name())

                    if not temp_doodad_surface and doodad.get_name():
                        self.load_doodad_surface(doodad.get_name(), doodad.get_type(), 1)
                        temp_doodad_surface = self.find_doodad_by_name(doodad.get_name())

                    temp_doodad_surface = pygame.transform.scale_by(temp_doodad_surface, 1)

            # Render the hex on the chunk surface
            # Calculate the position of the hex before rendering
            hex_size = (self.hex_surface_basic_size[0] * 1, self.hex_surface_basic_size[1] * 1)

            (tile_x, tile_y) = tile.position

            tile_offset_x = tile_x

            tile_y *= hex_size[1]
            tile_x *= hex_size[0]
            tile_x -= hex_size[0] * tile_offset_x // 4

            # Lower the hexagons on the odd positions
            if tile.position[0] % 2 == 1:
                tile_y += hex_size[1] // 2

            map_surf.blit(temp_hex_surface, (tile_x, tile_y))
            if tile.owner != -1 and temp_doodad_surface:
                map_surf.blit(temp_doodad_surface, (tile_x, tile_y))

        # Process all tiles
        for row in hex_map.hexmap:
            for tile in row:
                __draw_tile(self, tile, map_surf)

        return map_surf

    # Draw one tile to the screen
    def draw_tile(self, tile : Hex.Hex, new_color : tuple[int, int, int], chunk_surf : pygame.Surface):
        # Skip non-existing tiles
        if not tile:
            return

        # Change the inner color of the tile
        temp_hex_surface = self.find_hex_by_color(new_color)

        # Only generate new surface when needed
        if not temp_hex_surface:
            temp_hex_surface = self.add_hex_color(new_color)

        temp_hex_surface = pygame.transform.scale_by(temp_hex_surface, self.cached_zoom)

        # Draw the lack of tile
        if tile.owner == -1:
            temp_hex_surface = temp_hex_surface.copy()
            # If a background is loaded, use that
            if self.background_surface:
                temp_hex_surface.blit(self.background_surface, (0, 0), area=None, special_flags=pygame.BLEND_RGBA_MULT)
            # No background loaded, use the color
            else:
                temp_hex_surface.fill((255,255,255,0), special_flags=pygame.BLEND_RGBA_ADD)
                temp_hex_surface.fill(self.background_color, special_flags=pygame.BLEND_RGBA_MULT)

        else:
            # Load tile doodad surface
            temp_doodad_surface = None
            doodad = tile.get_doodad()
            if doodad:
                temp_doodad_surface = self.find_doodad_by_name(doodad.get_name())

                if not temp_doodad_surface and doodad.get_name():
                    self.load_doodad_surface(doodad.get_name(), doodad.get_type(), self.cached_zoom)
                    temp_doodad_surface = self.find_doodad_by_name(doodad.get_name())

                temp_doodad_surface = pygame.transform.scale_by(temp_doodad_surface, self.cached_zoom)

        # Render the hex on the chunk surface
        # Calculate the position of the hex before rendering
        hex_size = (self.hex_surface_basic_size[0] * self.cached_zoom, self.hex_surface_basic_size[1] * self.cached_zoom)

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
        if tile.owner != -1 and temp_doodad_surface:
            chunk_surf.blit(temp_doodad_surface, (tile_x, tile_y))

    # Generate all the chunks from the map
    def load_chunks(self, hexmap : HexMap.HexMap):
        if not hexmap:
            return

        self.hexmap = hexmap

        map_size = hexmap.dimensions

        tile_temp = self.visible_chunks[0][0]

        start_visible_size = (tile_temp.start_raw_position[0] * self.chunk_size[0], tile_temp.start_raw_position[1] * self.chunk_size[1])

        end_visible_size = (clamp(len(self.visible_chunks[0]) * self.chunk_size[0], 0, map_size[0]),
                            clamp(len(self.visible_chunks) * self.chunk_size[1], 0, map_size[1]))

        for y in range(start_visible_size[1], clamp(start_visible_size[1] + end_visible_size[1], 0, map_size[1])):
            for x in range(start_visible_size[0], clamp(start_visible_size[0] + end_visible_size[0], 0, map_size[0])):
                tile = hexmap.get_hexmap()[y][x]
                color = self.color_scheme[tile.owner]

                (x_chunk, y_chunk) = ((x - start_visible_size[0]) // self.chunk_size[0],
                                      (y - start_visible_size[1]) // self.chunk_size[1])
                chunk = self.visible_chunks[y_chunk][x_chunk]
                self.draw_tile(tile, color, chunk.chunk_surface)

    # Get all chunks inside the camera
    def get_visible_chunks(self):
        new_chunks = []
        if not self.chunks[0][0]:
            return

        chunk_size = (int(self.chunks[0][0].surface_size[0] * self.cached_zoom), int(self.chunks[0][0].surface_size[1] * self.cached_zoom))
        (pos_x_1, pos_y_1) = self.camera.get_corner_position()
        (pos_x_2, pos_y_2) = (pos_x_1 + self.camera.size[0], pos_y_1 + self.camera.size[1])

        # Add Hex chunk offset
        pos_x_1 += int((pos_x_1 // chunk_size[0] + 1) * self.hex_surface_basic_size[0] * self.cached_zoom // 4)
        pos_y_1 += int((pos_y_1 // chunk_size[1] + 1) * self.hex_surface_basic_size[1] * self.cached_zoom // 2)
        pos_x_2 += int((pos_x_2 // chunk_size[0] + 1) * self.hex_surface_basic_size[0] * self.cached_zoom // 4)
        pos_y_2 += int((pos_y_2 // chunk_size[1] + 1) * self.hex_surface_basic_size[1] * self.cached_zoom // 2)

        pos_1 = (pos_x_1, pos_y_1)
        pos_2 = (pos_x_2, pos_y_2)

        (pos_1_x, pos_1_y) = (pos_1[0] // chunk_size[0], pos_1[1] // chunk_size[1])
        (pos_2_x, pos_2_y) = (pos_2[0] // chunk_size[0], pos_2[1] // chunk_size[1])

        max_pos = (len(self.chunks[0]), len(self.chunks))

        # Clamp the positions to map size
        pos_1_x = clamp(pos_1_x - 1, 0, max_pos[0])
        pos_2_x = clamp(pos_2_x, 0, max_pos[0])
        pos_1_y = clamp(pos_1_y - 1, 0, max_pos[1])
        pos_2_y = clamp(pos_2_y, 0, max_pos[1])

        index = 0

        for y in range(pos_1_y, clamp(pos_2_y + 1, 0, max_pos[1])):
            new_chunks.append([])
            for x in range(pos_1_x, clamp(pos_2_x + 1, 0, max_pos[0])):
                current_chunk = self.chunks[y][x] 

                # Create surface for the new chunk
                new_chunks[index].append(current_chunk)
            index += 1

        different_lists = False

        if len(self.visible_chunks) != len(new_chunks) or len(self.visible_chunks[0]) != len(new_chunks[0]):
            different_lists = True
        else:
            for i in range(len(new_chunks)):
                for j in range(len(new_chunks[i])):
                    if self.visible_chunks[i][j] != new_chunks[i][j]:
                        different_lists = True
                        break

        if different_lists:
            # Delete the chunks no longer seen
            del_chunks = []
            for row in self.visible_chunks:
                for new_chunk in row:
                    found_chunk = False;
                    for y in range(len(new_chunks)):
                        if found_chunk == True:
                            break
                        for x in range(len(new_chunks[y])):
                            if new_chunk == new_chunks[y][x]:
                                found_chunk = True
                                break

                    if not found_chunk:
                        del_chunks.append(new_chunk)

            self.delete_chunks(del_chunks)

            # Draw the chunks seen
            self.visible_chunks.clear()
            self.visible_chunks[: + len(new_chunks)] = new_chunks
            for row in new_chunks:
                for chunk in row:
                    if chunk.chunk_surface == None:
                        new_chunk_size = (chunk.surface_size[0] * self.cached_zoom, chunk.surface_size[1] * self.cached_zoom)
                        chunk.chunk_surface = pygame.Surface(new_chunk_size, pygame.SRCALPHA)

            # NOTE: This will draw on the chunk regardless of it being already drawn onto or not. Must fix for boost in performance
            # NOTE: I don't like this method
            self.load_chunks(self.hexmap)

    # Delete a list of chunks
    def delete_chunks(self, chunks : list[HexChunk]):
        for ch in chunks:
            if isinstance(ch, HexChunk) and ch.chunk_surface:
                del ch.chunk_surface
                ch.chunk_surface = None
        chunks.clear()

    # Delete all visible chunks
    def clear_visible_chunks(self):
        for y in range(len(self.visible_chunks)):
            for chunk in self.visible_chunks[y]:
                if chunk.chunk_surface:
                    del chunk.chunk_surface
                    chunk.chunk_surface = None
            self.visible_chunks[y].clear()
        self.visible_chunks.clear()
        self.visible_chunks = []

    # Update a chunk from a changed tile
    def update_chunk(self, tile : Hex.Hex):
        (x_tile, y_tile) = tile.position
        chunk_surface = self.chunks[y_tile // self.chunk_size[1]][x_tile // self.chunk_size[0]].chunk_surface
        color = self.color_scheme[tile.owner]
        if chunk_surface:
            self.draw_tile(tile, color, chunk_surface)

    def update_list_chunks(self, tiles : list[Hex.Hex]):
        if tiles:
            for tile in tiles:
                if tile:
                    self.update_chunk(tile)

    # Draw all chunks to screen
    def draw_chunks(self):
        if not self.chunks[0][0]:
            return

        # Draw only the visible chunks
        for y in range(len(self.visible_chunks)):
            for x in range(len(self.visible_chunks[y])):
                current_chunk = self.visible_chunks[y][x]

                # Get the position for the next chunk
                x_chunk_pos = current_chunk.start_position[0] * self.cached_zoom - (current_chunk.start_raw_position[0] * self.hex_surface_basic_size[0] * self.cached_zoom // 4)
                y_chunk_pos = current_chunk.start_position[1] * self.cached_zoom - (current_chunk.start_raw_position[1] * self.hex_surface_basic_size[1] * self.cached_zoom // 2)

                # Apply camera offset
                x_chunk_pos -= self.camera.get_corner_position()[0]
                y_chunk_pos -= self.camera.get_corner_position()[1]

                if current_chunk.chunk_surface:
                    self.screen.blit(current_chunk.chunk_surface, (x_chunk_pos, y_chunk_pos))

