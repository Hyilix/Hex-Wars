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

screen_size = (1200, 800)
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Hex game")
clock = pygame.time.Clock() 
font = pygame.font.SysFont(None, 25)

game_handler = GameHandler.GameHandler()
game_handler.set_screen(screen)

# Set the first tab of the game
game_handler.switch_tab(GameHandler.CurrentTab.MAINMENU)

FPS = 144

game_handler.start_game()

while game_handler.get_game_running():
    screen.fill(colors.gray_very_dark)  # background color
    game_handler.draw_every_frame()
    keyboard_handled_this_frame = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            game_handler.pan_camera(pygame.mouse.get_pos())

        if event.type == pygame.QUIT:
            game_handler.stop_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Camera panning on R_CLICK
            if event.button == 3:
                game_handler.set_camera_pan_pivot()
                game_handler.set_camera_panning_mode(True)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                game_handler.set_camera_panning_mode(False)

        elif event.type == pygame.MOUSEWHEEL:
            game_handler.set_camera_zoom(event.y)

        keyboard_state = KeyboardState.KeyboardState()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                keyboard_state.parse_mouse_state(1, True)
                game_handler.gameplay_handle_mouse_action(pygame.mouse.get_pos(), True)
                game_handler.editor_handle_mouse_action(pygame.mouse.get_pos(), True)
                game_handler.menu_handle_mouse_action(pygame.mouse.get_pos(), True)

            if event.button == 2:
                keyboard_state.parse_mouse_state(2, True)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                keyboard_state.parse_mouse_state(1, False)

            if event.button == 2:
                keyboard_state.parse_mouse_state(2, False)

        if event.type == pygame.MOUSEMOTION:
            if keyboard_state.is_mouse1_down:
                game_handler.gameplay_handle_mouse_action(pygame.mouse.get_pos())
                game_handler.editor_handle_mouse_action(pygame.mouse.get_pos())
                game_handler.menu_handle_mouse_action(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            keyboard_state.parse_key_input(event.key, event.unicode, True)

        if event.type == pygame.KEYUP:
            keyboard_state.parse_key_input(event.key, event.unicode, False)

        if event.type == Events.KEYBOARD_CHANGED:
            if not keyboard_handled_this_frame:
                # Editor handle the keyboard
                game_handler.editor_handle_keyboard()
                game_handler.gameplay_handle_keyboard()

                keyboard_handled_this_frame = True

        if event.type == Events.MAP_CHANGED:
            game_handler.set_new_map_editor()
            game_handler.set_new_map_gameplay()
            game_handler.reload_renderer()

        if event.type == Events.CENTER_CAMERA:
            game_handler.center_camera()

    # Update display
    pygame.display.flip()

    clock.tick(FPS)  # limit to FPS frames per second
    pygame.display.set_caption("Hex Game FPS: " + str(round(clock.get_fps(), 1)))

pygame.quit()

