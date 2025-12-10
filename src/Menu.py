import pygame

import button
import colors
import ButtonHandler

# Super class for all the menus in the game
class Menu:
    def __init__(self, screen):
        self.__screen = screen
        self.__buttons : list[button.Button] = []

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

class MapPicker(Menu):
    def __init__(self, screen):
        super().__init__(screen)

