import pygame
from pygame.locals import *
import Doodads
import sys
from Player import Player
import button
import HexMap
import GameRenderer
from colors import *
import colors

pygame.init()

screen = pygame.display.set_mode((800, 600), RESIZABLE)

pygame.display.set_caption("Hex game")
clock = pygame.time.Clock() 
font = pygame.font.SysFont(None, 20)

kkk: int = 0
playercount: int = 0


butter = [button.Button]
playerlist: list[Player] = []
playercolor: list[tuple[int, int, int]] = []
playercolor.append(red)
playercolor.append(green)
playercolor.append(cyan)
playercolor.append(purple)

quit_but = button.Button(10, 10)
t1 = button.Button(70, 10)
t2 = button.Button(130, 10)
farm = button.Button(190, 10)
pesant = button.Button(250, 10)
spear = button.Button(310, 10)
knight = button.Button(370, 10)
elite = button.Button(430, 10)
start = button.Button(10, 50)
end_turn = button.Button(10,50)
add_player = button.Button(70,10)

# Create a GameRenderer
color_scheme = [gray_light, red, blue, green, yellow]
renderer = GameRenderer.GameRenderer(screen, color_scheme)

renderer.load_hex_surface(4)

# Create and fill a map
test_hex_map = HexMap.HexMap(20, 10, 0)

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
                if (start.buttonBG.collidepoint(event.pos) and kkk == 0):
                    print("start nigger!")
                    kkk = 1    

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if (t1.buttonBG.collidepoint(event.pos) and kkk == 1):
                    print("tower1!")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if t2.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("tower2!")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if farm.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("work farm!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if pesant.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("pesant!")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if spear.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("spear!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if knight.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("knight!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if elite.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("elite!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if end_turn.buttonBG.collidepoint(event.pos) and kkk == 1:
                    print("end turn!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if add_player.buttonBG.collidepoint(event.pos) and kkk == 0 and playercount < 4:
                    playercount += 1
                    newplayer = Player(6,12, playercount, playercolor[playercount - 1])
                    playerlist.append(newplayer)
                    print("player!")
                elif add_player.buttonBG.collidepoint(event.pos) and kkk == 0:
                    print("max players reached")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if spear.buttonBG.collidepoint(event.pos):
                    print(str(playercount) + " spear! " + str(len(playerlist)))

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:  # Left mouse button
        #         mouse_pos = event.pos
        #         if spear.buttonBG.collidepoint(event.pos):
        #             print("spear!")


    # 3. draw everything
    screen.fill((150, 250, 50))  # background color
    # draw_button()
    renderer.draw_tiles(test_hex_map.hexmap)

    quit_but.draw(screen, font, white, red, white, "QUIT")
    
    t2.draw(screen,font, white, blue, white, "Tower2")
    farm.draw(screen,font, white, blue, white, "Farm")
    pesant.draw(screen,font, white, blue, white, "Pesant")
    spear.draw(screen,font, white, blue, white, "Spear")
    knight.draw(screen,font, white, blue, white, "Knight")
    elite.draw(screen,font, white, blue, white, "Elite")
    if(kkk == 0):
        start.draw(screen,font, white, blue, white, "Start")
        add_player.draw(screen,font, white, blue, white, "add play")
    else:
        end_turn.draw(screen,font, white, blue, white, "End turn")
        t1.draw(screen,font, white, blue, white, "Tower1")
    pygame.display.flip()      # update display

    clock.tick(60)  # limit to 60 frames per second

pygame.quit()
