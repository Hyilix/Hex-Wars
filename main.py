import pygame
from pygame.locals import *
import Doodads
import sys
from button import *
from colors import *


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
    quit_but.draw(screen, font, white, red, white, "quit")
    t1.draw(screen,font, white, blue, white, "Tower1")
    t2.draw(screen,font, white, blue, white, "Tower2")
    farm.draw(screen,font, white, blue, white, "Farm")
    pesant.draw(screen,font, white, blue, white, "Pesant")
    spear.draw(screen,font, white, blue, white, "Spear")
    knight.draw(screen,font, white, blue, white, "Knight")
    elite.draw(screen,font, white, blue, white, "Elite")
    pygame.display.flip()      # update display

    clock.tick(60)  # limit to 60 frames per second

pygame.quit()