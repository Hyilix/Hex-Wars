import pygame

class Button:
    def __init__(self, a , b):
        self.__a = a
        self.__b = b
        self.buttonBG = pygame.Rect(self.__a, self.__b, 50, 25)
        self.button = pygame.Rect(self.__a + 2, self.__b + 2, 46, 21)

    def draw(self, screen, font, color1, color2, color3, text):
        pygame.draw.rect(screen, color1, self.buttonBG)
        pygame.draw.rect(screen, color2, self.button)
        # pygame.draw.rect(screen, (0, 128, 255), quit_button)
        text_surface = font.render(text, True, color3)
        text_rect = text_surface.get_rect(center=self.buttonBG.center)
        screen.blit(text_surface, text_rect)

