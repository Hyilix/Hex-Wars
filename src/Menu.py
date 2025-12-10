import pygame

import button
import colors
import ButtonHandler

DEFAULT_FONT_PATH = "../assets/fonts/"

# Super class for all the menus in the game
class Menu:
    def __init__(self, screen):
        self.__screen = screen
        self.__buttons : list[button.Button] = []

        self.__title = "Hex Wars"

        self.default_font = DEFAULT_FONT_PATH + 'Orbitron.ttf'
        self.button_font = pygame.font.Font(self.default_font, 60)

    def get_screen(self):
        return self.__screen

    def get_buttons(self):
        return self.__buttons

    def add_buttons(self, buttons):
        self.__buttons = buttons

    def spread_buttons(self):
        y_offset = 20
        no_buttons = len(self.__buttons)

        # The half of the screen
        x_pos = self.__screen.get_size()[0] // 2 - self.__buttons[0].get_size()[0] // 2
        y_pos = self.__screen.get_size()[1] // 2

        y_pos -= (self.__buttons[0].get_size()[1] + y_offset) * (no_buttons // 2)
        if no_buttons % 2 == 1:
            y_pos -= self.__buttons[0].get_size()[1] // 2

        y_step = self.__buttons[0].get_size()[1] + y_offset

        for button in self.__buttons:
            button.change_pos((x_pos, y_pos))
            y_pos += y_step

    def draw_buttons(self):
        for button in self.__buttons:
            button.draw(self.__screen)

    def draw_title(self):
        text = self.button_font.render(self.__title, True, colors.gray_light)
        text_rect = text.get_rect()

        x_pos = self.__screen.get_size()[0] // 2
        y_pos = self.__screen.get_size()[1] // 10

        text_rect.center = (x_pos, y_pos)

        self.__screen.blit(text, text_rect)

    def buttons_click_action(self, mouse_pos : tuple[int, int], caller):
        for button in self.__buttons:
            if button.check_mouse_collision(mouse_pos):
                button.call_function(caller, button)

# Main menu, where the game opens
class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

# Lobby menu, where the players are being prepared
class Lobby(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        self.color_scheme = [colors.gray_light, None, None, None, None, None, None]

    def add_buttons(self, buttons):
        self.get_buttons().extend(buttons)

    def spread_buttons(self):
        x_offset = 20
        no_buttons = len(self.get_buttons())

        # The half of the screen
        x_pos = self.get_screen().get_size()[0] // 2
        y_pos = self.get_screen().get_size()[1] // 2 - self.get_buttons()[0].get_size()[1] // 2

        x_pos -= (self.get_buttons()[0].get_size()[0] + x_offset) * (no_buttons // 2)
        if no_buttons % 2 == 1:
            x_pos -= self.get_buttons()[0].get_size()[0] // 2

        x_step = self.get_buttons()[0].get_size()[0] + x_offset

        for button in self.get_buttons():
            button.change_pos((x_pos, y_pos))
            x_pos += x_step

    def open_colors_panel(self):
        available_colors = colors.available_colors

class MapPicker(Menu):
    def __init__(self, screen):
        super().__init__(screen)

