from contextlib import contextmanager
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

    def draw(self, screen):
        pass

# Button made from 2 rectangle
class SimpleButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], content : str, func = None):
        super().__init__(pos, size, func)

        self.content = content

        self.border = pygame.Rect(pos, size)
        self.color = colors.gray_light
        self.width = 2

        self.DEFAULT_FONT = 'freesansbold.ttf'
        self.BUTTON_FONT = pygame.font.Font(self.DEFAULT_FONT, 16)

    def render_text(self, screen):
        text = self.BUTTON_FONT.render(self.content, True, colors.gray_light)
        text_rect = text.get_rect()

        text_rect.update(self.get_pos(), self.get_size())

        screen.blit(text, text_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.border, width=self.width)
        self.render_text(screen)

# Button having a texture
class TextureButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func = None):
        super().__init__(pos, size, func)

        self.__is_highlighted = False
        self.__is_doodad = False

        # Information about button texture (including highlight)
        self.__texture : pygame.Surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__highlight = pygame.Rect(pos, size)

        self.__highlight_width = 3

    def set_doodad_state(self):
        self.__is_doodad = True

    def is_doodad(self):
        return self.__is_doodad

    def change_pos(self, new_pos : tuple[int, int]):
        super().change_pos(new_pos)
        self.__highlight.x = new_pos[0]
        self.__highlight.y = new_pos[1]

    def load_texture(self, path : str):
        self.__texture = pygame.image.load(path)

    def draw(self, screen):
        screen.blit(self.__texture, self.get_pos())
        if self.__is_highlighted:
            pygame.draw.rect(screen, colors.yellow, self.__highlight, width=self.__highlight_width)

    def toggle_highlight(self):
        self.__is_highlighted = not self.__is_highlighted

    def set_highlight(self, is_highlight : bool = False):
        self.__is_highlighted = is_highlight

# Button having a slider
class SliderButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func = None):
        super().__init__(pos, size, func)

        self.__border_color = colors.gray_light
        self.__slider_color = colors.gray_light

        self.__border_width = 2

        # 0-100 procent of fill
        self.__slider_progress = 0

