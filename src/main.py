import pygame
from pygame.locals import *
import Doodads
import sys

import HexMap
import GameRenderer
import colors

pygame.init()

screen = pygame.display.set_mode((800, 600), RESIZABLE)

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

# Create a GameRenderer
color_scheme = [colors.gray_light, colors.red, colors.blue, colors.green, colors.yellow]
renderer = GameRenderer.GameRenderer(screen, color_scheme)

renderer.load_hex_surface(4)

# Create and fill a map
test_hex_map = HexMap.HexMap(10, 6, 0)

running = True
while running:
    # 1. handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
             if quit_button1.collidepoint(event.pos):
                  pygame.quit()
                  sys.exit()
    # 2. update game logic
    # (e.g. move player, check collisions)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                print(f"Mouse clicked at: {mouse_pos}")
                if quit_button1.collidepoint(event.pos):
                    print("Button clicked!")

    # 3. draw everything
    screen.fill((50, 50, 50))  # background color
    # draw_button()
    renderer.draw_map(test_hex_map)
    pygame.display.flip()      # update display

    clock.tick(60)  # limit to 60 frames per second

pygame.quit()
