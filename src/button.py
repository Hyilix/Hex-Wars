from os import posix_fadvise
import pygame

import colors
import Collisions_2d

# Super class for all types of buttons
class Button:
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func):
        self.__pos = pos
        self.__size = size
        self.__function = func

    def change_pos(self, new_pos : tuple[int, int]):
        self.__pos = new_pos

    def change_size(self, new_size : tuple[int, int]):
        self.__size = new_size

    def get_pos(self):
        return self.__pos

    def get_size(self):
        return self.__size

    def change_function(self, new_func):
        self.__function = new_func

    def call_function(self, *args, **kwargs):
        if self.__function is not None:
            self.__function(*args, **kwargs)

    # Determine if mouse is on button
    def check_mouse_collision(self, mouse_pos : tuple[int, int]):
        return Collisions_2d.point_rect(mouse_pos, self.__pos, self.__size)

# Button made from 2 rectangles
class SimpleButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func = None):
        super().__init__(pos, size, func)
        self.buttonBG = pygame.Rect(self.__pos, self.__size)
        self.button = pygame.Rect(self.__pos[0] + 2, self.__pos[1] + 2, self.__size[0] - 4, self.__size[1] - 4)

    def draw(self, screen, font, color1, color2, color3, text):
        pygame.draw.rect(screen, color1, self.buttonBG)
        pygame.draw.rect(screen, color2, self.button)
        # pygame.draw.rect(screen, (0, 128, 255), quit_button)
        text_surface = font.render(text, True, color3)
        text_rect = text_surface.get_rect(center=self.buttonBG.center)
        screen.blit(text_surface, text_rect)

# Button having a texture
class TextureButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func = None):
        super().__init__(pos, size, func)

        # Information about button highlight
        self.__highlight_color = colors.white
        self.__highlight_alpha = 200
        self.__is_highlighted = False

        # Information about button texture (including highlight)
        self.__texture : pygame.Surface = pygame.Surface(self.__size, pygame.SRCALPHA)

    def load_texture(self, texture : pygame.Surface):
        pass

# Button having a slider
class SliderButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func = None):
        super().__init__(pos, size, func)

        self.__background_color = colors.gray_light
        self.__slider_color = colors.gray_dark

        # 0-100 procent of fill
        self.__slider = 0

