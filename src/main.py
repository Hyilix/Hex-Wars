import pygame
from pygame.locals import *
import Doodads
import sys
import copy

import MapHandling
import KeyboardState

from collections import deque

import GameHandler
import HexMap
import GameRenderer
import colors

import Events
import Editor

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
test_hex_map = HexMap.HexMap(30, 30, 0)
renderer.init_chunks(test_hex_map.dimensions)
renderer.get_visible_chunks()
renderer.load_chunks(test_hex_map)

test_editor = Editor.Editor(renderer, test_hex_map, screen_size)

FPS = 144

running = True
while running:
    screen.fill(renderer.background_color)  # background color
    renderer.draw_chunks()
    test_editor.render_tabs(screen)
    keyboard_handled_this_frame = False

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
            # Camera panning on R_CLICK
            if event.button == 3:
                camera_test.pan_pivot = pygame.mouse.get_pos()
                camera_test.panning_mode = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                camera_test.panning_mode = False

        elif event.type == pygame.MOUSEWHEEL:
            renderer.set_zoom(round(event.y, 1) * renderer.zoom_settings[2] + renderer.current_zoom)

        keyboard_state = KeyboardState.KeyboardState()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # TODO: Remove button test
                mouse_pos = event.pos
                print(f"Mouse clicked at: {mouse_pos}")
                if quit_button1.collidepoint(event.pos):
                    print("Button clicked!")

                keyboard_state.parse_mouse_state(1, True)

            if event.button == 2:
                keyboard_state.parse_mouse_state(2, True)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                keyboard_state.parse_mouse_state(1, False)

            if event.button == 2:
                keyboard_state.parse_mouse_state(2, False)

        if event.type == pygame.MOUSEMOTION:
            if keyboard_state.is_mouse1_down:
                mouse_pos = event.pos

                tile_pos = camera_test.get_tile_at_position(mouse_pos)
                # Check if tile is within bounds
                if tile_pos[0] >= 0 and tile_pos[0] < test_hex_map.dimensions[0]:
                    if tile_pos[1] >= 0 and tile_pos[1] < test_hex_map.dimensions[1]:
                        current_tile = test_hex_map.get_tile_at_position(tile_pos)
                        test_editor.handle_mouse_action(mouse_pos, current_tile)

        if event.type == pygame.KEYDOWN:
            keyboard_state.parse_key_input(event.key, True)

        if event.type == pygame.KEYUP:
            keyboard_state.parse_key_input(event.key, False)

        if event.type == Events.KEYBOARD_CHANGED:
            if not keyboard_handled_this_frame:
                # Editor handle the keyboard
                test_editor.handle_keyboard_action(screen)

                keyboard_handled_this_frame = True

    # Update display
    pygame.display.flip()

    clock.tick(FPS)  # limit to FPS frames per second
    pygame.display.set_caption("Hex Game FPS: " + str(round(clock.get_fps(), 1)))

pygame.quit()

        # if event.type == pygame.KEYDOWN:
        #     # Test map saving
        #     if event.key == pygame.key.key_code('k'):
        #         MapHandling.save_game({
        #             "Name": "Map Test 1",
        #             "Players": [],
        #             "CurrentPlayer": 0,
        #             "Map": test_hex_map
        #                                }, "test_map_1")
        #
        #     # Test map loading
        #     elif event.key == pygame.key.key_code('l'):
        #         config : dict = MapHandling.load_game("test_map_1")
        #
        #         test_hex_map = copy.deepcopy(config.get("Map"))
        #
        #         renderer.reload_renderer(test_hex_map)
        #         # renderer.clear_visible_chunks()
        #         # renderer.get_visible_chunks()
        #         # print(f"Map: {test_hex_map.hexmap[0][0].doodad}")
        #
        #     elif event.key == pygame.key.key_code('z'):
        #         print("Undo")
        #         test_editor.action_handler.undo_action_last()
        #         renderer.load_chunks(test_hex_map)
        #
        #     elif event.key == pygame.key.key_code('y'):
        #         print("Redo")
        #         test_editor.action_handler.redo_last_action()
        #         renderer.load_chunks(test_hex_map)
