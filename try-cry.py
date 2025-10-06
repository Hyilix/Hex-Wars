import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hex game")
clock = pygame.time.Clock() 

button_rect = pygame.Rect(300, 250, 200, 100)

running = True
while running:
    # 1. handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. update game logic
    # (e.g. move player, check collisions)

    if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                print(f"Mouse clicked at: {mouse_pos}")
                if button_rect.collidepoint(event.pos):
                    print("Button clicked!")

    # 3. draw everything
    screen.fill((50, 50, 50))  # background color
    pygame.draw.rect(screen, (0, 128, 255), button_rect)
    pygame.display.flip()      # update display

    clock.tick(60)  # limit to 60 frames per second

pygame.quit()