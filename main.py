import pygame
from pygame.locals import *
import Doodads
import sys
from button import *
from colors import *
import math
import random

# Simple unit test
UnitTest = Doodads.UnitTier3(1)

print(UnitTest.income)

pygame.init()

screen = pygame.display.set_mode((800, 600), RESIZABLE)

pygame.display.set_caption("Hex game")
clock = pygame.time.Clock() 
font = pygame.font.SysFont(None, 20)

quit_but = Button(10, 10)
t1 = Button(70, 10)
t2 = Button(130, 10)
farm = Button(190, 10)
pesant = Button(250, 10)
spear = Button(310, 10)
knight = Button(370, 10)
elite = Button(430, 10)

# quit_button1 = pygame.Rect(10, 10, 50, 25)
# quit_button2 = pygame.Rect(12, 12, 46, 21)
# quit_button3 = pygame.Rect(10, 10, 50, 25)

# def draw_button():
#     pygame.draw.rect(screen, red, quit_button1)
#     pygame.draw.rect(screen, black, quit_button2)
#     # pygame.draw.rect(screen, (0, 128, 255), quit_button)
#     text_surface = font.render('Quit', True, (255, 255, 255))
#     text_rect = text_surface.get_rect(center=quit_button1.center)
#     screen.blit(text_surface, text_rect)
HEX_COLOR = (100, 200, 150)
hex_radius = 40
hex_height = math.sqrt(3) * hex_radius
hex_width = 2.1 * hex_radius

def draw_hexagon(surface, color, position):
    x, y = position
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        px = x + hex_radius * math.cos(angle_rad)
        py = y + hex_radius * math.sin(angle_rad)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points, 2)

holes = {(1, 2), (3, 4), (4, 1)}

def draw_hex_grid(rows, cols):
    for row in range(rows):
        for col in range(cols):
            if (row, col) in holes:
            # if random.random() < 0.1:
                continue
            x = col * hex_width * 3/4 + 100
            y = row * hex_height + (col % 2) * (hex_height / 2) + 100
            draw_hexagon(screen, HEX_COLOR, (x, y))

running = True
while running:
    # 1. handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
             if quit_but.buttonBG.collidepoint(event.pos):
                  pygame.quit()
                  sys.exit()
    # 2. update game logic
    # (e.g. move player, check collisions)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                print(f"Mouse clicked at: {mouse_pos}")
                if quit_but.buttonBG.collidepoint(event.pos):
                    print("Button clicked!")

    # 3. draw everything
    screen.fill((50, 50, 50))  # background color
    quit_but.draw(screen, font, white, red, white, "QUIT")
    t1.draw(screen,font, white, blue, white, "Tower1")
    t2.draw(screen,font, white, blue, white, "Tower2")
    farm.draw(screen,font, white, blue, white, "Farm")
    pesant.draw(screen,font, white, blue, white, "Pesant")
    spear.draw(screen,font, white, blue, white, "Spear")
    knight.draw(screen,font, white, blue, white, "Knight")
    elite.draw(screen,font, white, blue, white, "Elite")
    draw_hex_grid(5, 7)
    pygame.display.flip()      # update display

    clock.tick(60)  # limit to 60 frames per second

pygame.quit()