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

    def clear_buttons(self):
        self.__buttons = []

    def spread_buttons(self, y_offset = 0, start_index = 0):
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

        self.clear_buttons()

        self.color_scheme = [colors.gray_light, None, None, None, None, None, None]
        self.available_colors = colors.available_colors

    def add_buttons(self, buttons):
        self.get_buttons().extend(buttons)

    def __get_next_available_color(self):
        for i in range(len(self.available_colors)):
            color = self.available_colors[i]
            if color not in self.color_scheme:
                return color, i

        return None, None

    def spread_buttons(self, y_offset : int = 0, start_index : int = 0):
        x_offset = 20
        no_buttons = len(self.get_buttons())
        no_buttons -= start_index

        # The half of the screen
        x_pos = self.get_screen().get_size()[0] // 2
        y_pos = self.get_screen().get_size()[1] // 2 - self.get_buttons()[start_index].get_size()[1] // 2
        y_pos += y_offset

        x_pos -= (self.get_buttons()[start_index].get_size()[0] + x_offset) * (no_buttons // 2)
        if no_buttons % 2 == 1:
            x_pos -= self.get_buttons()[start_index].get_size()[0] // 2

        x_step = self.get_buttons()[start_index].get_size()[0] + x_offset

        for i in range(start_index, len(self.get_buttons())):
            button = self.get_buttons()[i]
            button.change_pos((x_pos, y_pos))
            x_pos += x_step

    def move_join_next(self):
        join_button = self.get_buttons()[-1]

        button_index = 0

        for i in range(1, len(self.color_scheme)):
            if self.color_scheme[i] == None:
                button_index = i
                break

        if button_index > 0:
            self.get_buttons()[11].active = False
            print(f"Found hex, {button_index}")
            join_button.active = True

            # Get the hex above it
            ref_button = self.get_buttons()[button_index - 1]

            new_x = ref_button.get_pos()[0]
            new_y = ref_button.get_pos()[1]

            # Change the position of the join button
            join_button.change_pos((new_x, new_y + 200))

            # Activate the remove button
            if button_index > 1:
                self.get_buttons()[button_index - 2 + 6].active = True
        else:
            self.get_buttons()[11].active = True
            join_button.active = False

        print(f"new color scheme: {self.color_scheme}")

    def join_player(self):
        button_index = 0

        for i in range(1, len(self.color_scheme)):
            if self.color_scheme[i] == None:
                button_index = i
                break

        # Set next available color
        self.color_scheme[button_index], color_index = self.__get_next_available_color()

        self.get_buttons()[button_index - 1].change_color(self.color_scheme[button_index])
        self.get_buttons()[button_index - 1].set_color_index(color_index)

    def remove_player(self, button):
        # Find button
        button_index = -1

        # Find the index of the button
        for i in range(len(self.get_buttons())):
            loaded_button = self.get_buttons()[i]
            if button == loaded_button:
                button_index = i
                break

        # Found no button
        if button_index == -1:
            return

        print(f"new color scheme: {self.color_scheme}")

        # Shift the players
        color_index = button_index - 5
        del self.color_scheme[color_index]
        self.color_scheme.append(None)

        print(f"new color scheme: {self.color_scheme}, index: {color_index}")

        for i in range(len(self.color_scheme)):
            color = self.color_scheme[i]
            if color == None:
                print(f"The index i found is {i}")
                self.get_buttons()[i - 1 + 6].active = False
                break

        self.move_join_next()

        for i in range(1, len(self.color_scheme)):
            color = self.color_scheme[i]
            if color != None:
                self.get_buttons()[i - 1].change_color(color)
                self.get_buttons()[i - 1].set_color_index(self.available_colors.index(color))
            else:
                self.get_buttons()[i - 1].change_color(colors.shader_color)
                self.get_buttons()[i - 1].set_color_index(-1)

    def change_next_color(self, button):
        if button.get_old_color() == colors.shader_color:
            return

        # Find button
        button_index = -1

        # Find the index of the button
        for i in range(len(self.get_buttons())):
            loaded_button = self.get_buttons()[i]
            if button == loaded_button:
                button_index = i
                break

        # Found no button
        if button_index == -1:
            return

        no_colors = len(self.available_colors)

        button.inc_color_index()
        if button.get_color_index() >= no_colors:
            button.set_color_index(0)

        secluded_color_scheme = []
        for i in range(1, len(self.color_scheme)):
            if i - 1 != button_index:
                secluded_color_scheme.append(self.color_scheme[i])

        while (self.available_colors[button.get_color_index()] in secluded_color_scheme):
            button.inc_color_index()
            if button.get_color_index() >= no_colors:
                button.set_color_index(0)

        button.change_color(self.available_colors[button.get_color_index()])
        self.color_scheme[button_index + 1] = self.available_colors[button.get_color_index()]

    def get_color_scheme(self):
        return self.color_scheme

class MapPicker(Menu):
    def __init__(self, screen):
        super().__init__(screen)

