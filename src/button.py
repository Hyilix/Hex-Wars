from contextlib import contextmanager
from os import posix_fadvise
import pygame

import colors
import Collisions_2d
from utils import clamp

DEFAULT_FONT_PATH = "../assets/fonts/"

# Super class for all types of buttons
class Button:
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], func):
        self.__pos = pos
        self.__size = size
        self.__function = func

        self.is_highlighted = None

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
        self.button_font = pygame.font.Font(self.DEFAULT_FONT, 16)

    def change_pos(self, new_pos: tuple[int, int]):
        super().change_pos(new_pos)
        self.border.topleft = new_pos

    def render_text(self, screen):
        text = self.button_font.render(self.content, True, colors.gray_light)
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

        self.is_highlighted = False
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
        if self.is_highlighted:
            pygame.draw.rect(screen, colors.yellow, self.__highlight, width=self.__highlight_width)

    def toggle_highlight(self):
        self.is_highlighted = not self.is_highlighted

    def set_highlight(self, is_highlight : bool = False):
        self.is_highlighted = is_highlight

# Button having a slider
class SliderButton(Button):
    def __init__(self, pos : tuple[int, int], size : tuple[int, int], content : str, func = None):
        super().__init__(pos, size, func)

        self.content = content

        self.__border = pygame.Rect(pos, size)
        self.__border_color = colors.ui_gray

        self.__slider = pygame.Rect(pos, (16, size[1]))
        self.__slider_color = colors.gray_light

        self.__border_width = 4

        # 0-100 procent of fill
        self.slider_progress = 0

        self.default_font = DEFAULT_FONT_PATH + 'Orbitron.ttf'
        self.button_font = pygame.font.Font(self.default_font, 30)

    def change_progress(self, new_progress):
        self.slider_progress = clamp(new_progress, 0, 100)
        self.__slider.left = self.__border.left + int(self.slider_progress / 100 * (self.__border.width - self.__slider.width))

    def change_pos(self, new_pos: tuple[int, int]):
        super().change_pos(new_pos)
        self.__border.topleft = new_pos
        self.__slider.topleft = new_pos

    def render_text(self, screen):
        text = self.button_font.render(self.content, True, colors.ui_gray)
        text_rect = text.get_rect()

        text_rect.center = self.__border.center

        screen.blit(text, text_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.__border_color, self.__border, width=self.__border_width)
        self.render_text(screen)
        pygame.draw.rect(screen, self.__slider_color, self.__slider)

    def check_mouse_collision(self, mouse_pos: tuple[int, int]):
        is_mouse_inside = super().check_mouse_collision(mouse_pos)

        if is_mouse_inside:
            start_pos = self.__border.left
            end_pos = self.__border.left + self.__border.width - self.__slider.width
            distance = end_pos - start_pos

            mouse_progress = mouse_pos[0] - start_pos

            self.change_progress(int(mouse_progress / distance * 100))

        return is_mouse_inside

