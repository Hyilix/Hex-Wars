import pygame
from pygame.locals import *
import Doodads
import sys
import copy

import MapHandling

from collections import deque

import GameHandler
import HexMap
import GameRenderer
import colors

pygame.init()

screen_size = (1000, 600)
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Hex game")
clock = pygame.time.Clock() 
font = pygame.font.SysFont(None, 25)

quit_button1 = pygame.Rect(10, 10, 50, 25)
quit_button2 = pygame.Rect(12, 12, 46, 21)
quit_button3 = pygame.Rect(10, 10, 50, 25)


def draw_button():
    pygame.draw.rect(screen, (200, 200, 200), quit_button1)
    pygame.draw.rect(screen, (0, 0, 0), quit_button2)
    # pygame.draw.rect(screen, (0, 128, 255), quit_button)
    text_surface = font.render('Quit', True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=quit_button1.center)
    screen.blit(text_surface, text_rect)

# Create a Camera
# Note, use the window size as camera default
camera_test = GameRenderer.Camera(screen_size, (0, 0), 1)

# Create a GameRenderer
color_scheme = [colors.gray_dark, colors.red, colors.blue, colors.green, colors.yellow, colors.purple, colors.cyan, colors.pink]
renderer = GameRenderer.GameRenderer(screen, camera_test, color_scheme)

renderer.load_hex_surface("HexTile.png", 1)

# Create and fill a map
test_hex_map = HexMap.HexMap(10, 20, 0)
renderer.init_chunks(test_hex_map.dimensions)
renderer.get_visible_chunks()
renderer.load_chunks(test_hex_map)

FPS = 144

running = True
while running:
    # 1. handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            new_coord = pygame.mouse.get_pos()

            # Pan the camera
            if camera_test.panning_mode == True:
                win_size = pygame.display.get_window_size()
                (x_dir, y_dir) = (new_coord[0] - camera_test.pan_pivot[0], new_coord[1] - camera_test.pan_pivot[1])
                camera_test.add_direction((x_dir, y_dir))
                renderer.get_visible_chunks()

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # if quit_button1.collidepoint(event.pos):
            #     pygame.quit()
            #     sys.exit()
            # Camera panning on R_CLICK
            if event.button == 3:
                camera_test.pan_pivot = pygame.mouse.get_pos()
                camera_test.panning_mode = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                camera_test.panning_mode = False
    #2. update game logic
    # (e.g. move player, check collisions)

        elif event.type == pygame.MOUSEWHEEL:
            renderer.set_zoom(round(event.y, 1) * renderer.zoom_settings[2] + renderer.current_zoom)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                print(f"Mouse clicked at: {mouse_pos}")
                if quit_button1.collidepoint(event.pos):
                    print("Button clicked!")

                tile_pos = camera_test.get_tile_at_position(mouse_pos)
                current_tile = test_hex_map.get_tile_at_position(tile_pos)
                current_tile.set_owner(1)

                test_temp_doodad = Doodads.UnitTier2(1)
                current_tile.set_doodad(test_temp_doodad)

                renderer.update_chunk(current_tile)

        if event.type == pygame.KEYDOWN:
            # Test map saving
            if event.key == pygame.key.key_code('k'):
                MapHandling.save_game({
                    "Name": "Map Test 1",
                    "Players": [],
                    "CurrentPlayer": 0,
                    "Map": test_hex_map
                                       }, "test_map_1")

            # Test map loading
            elif event.key == pygame.key.key_code('l'):
                config : dict = MapHandling.load_game("test_map_1")

                test_hex_map = copy.deepcopy(config.get("Map"))

                renderer.reload_renderer(test_hex_map)
                # renderer.clear_visible_chunks()
                # renderer.get_visible_chunks()
                # print(f"Map: {test_hex_map.hexmap[0][0].doodad}")

    # 3. draw everything
    screen.fill((50, 50, 50))  # background color
    # draw_button()
    renderer.draw_chunks()
    pygame.display.flip()      # update display

    clock.tick(FPS)  # limit to 60 frames per second
    pygame.display.set_caption("Hex Game FPS: " + str(round(clock.get_fps(), 1)))
    # print(f"Current FPS = {clock.get_fps()}")

pygame.quit()
