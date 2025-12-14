import pygame
from enum import Enum

import button
import Collisions_2d

# Enum class for representing current tab opened
class TabMenu(Enum):
    WORLD = 10

# Tab super class for all the editor's tabs
class Tab:
    def __init__(self, position : tuple[int, int], size : tuple[int, int], background_color : tuple[int, int, int, int]):
        self.__pos = position
        self.__size = size

        self.__is_clicked_inside = False
        self.__buttons : list[button.Button] = []
        self.__background_color = background_color

        self.__color_surface : pygame.Surface
        self.create_color_surface()

    # Get is_clicked_inside state
    def get_clicked_inside(self):
        return self.__is_clicked_inside

    # Clear is_clicked_inside state
    def clear_clicked_inside(self):
        self.__is_clicked_inside = False

    def get_buttons(self):
        return self.__buttons

    def buttons_click_action(self, mouse_pos : tuple[int, int], editor):
        for button in self.__buttons:
            if button.check_mouse_collision(mouse_pos):
                button.call_function(editor, button)

    # Determine if the mouse is inside the tab
    def click_action(self, mouse_pos : tuple[int, int]):
        self.__is_clicked_inside = Collisions_2d.point_rect(mouse_pos, self.__pos, self.__size)
        return self.__is_clicked_inside

    # Get the buttons into the internal buttons list.
    # Buttons' positions don't matter, as they will be set by spread_buttons method
    def fill_buttons_list(self, buttons : list[button.Button]):
        self.__buttons = buttons.copy()

    def add_buttons(self, buttons : list[button.Button]):
        last_pos = self.__buttons[-1].get_pos()

        last_y = last_pos[1] + 2 * buttons[0].get_size()[1]
        print(f"Last y pos: {last_y}")

        for button in buttons:
            button.change_pos((self.__size[0] // 2 - button.get_size()[0] // 2, last_y))
            last_y += button.get_size()[1] + 10
            self.__buttons.append(button)

    # Spread the buttons evenly on the tab, having equal distance between them on the x-axis
    def spread_buttons(self, buttons_per_row : int = 0):
        y_offset = 10
        x_offset = 10

        if buttons_per_row == 0:
            # Calculate how many buttons can fit with proper spacing
            button_width = self.__buttons[0].get_size()[0]
            available_width = self.__size[0] - (2 * x_offset)

            # Estimate spacing (use a minimum spacing value)
            min_spacing = 10
            buttons_per_row = max(1, available_width // (button_width + min_spacing))

        # Calculate spacing between buttons
        available_width = self.__size[0] - (2 * x_offset)
        button_width = self.__buttons[0].get_size()[0]

        # Calculate spacing to distribute buttons evenly
        total_button_width = button_width * buttons_per_row
        remaining_space = available_width - total_button_width
        spacing = remaining_space // (buttons_per_row + 1)

        # Set button positions
        row = 0
        col = 0
        for button in self.__buttons:
            x_pos = self.__pos[0] + x_offset + spacing + col * (button_width + spacing)
            y_pos = self.__pos[1] + y_offset + row * (button.get_size()[1] + y_offset)
            button.change_pos((x_pos, y_pos))

            # Move to next column, or wrap to next row
            col += 1
            if col == buttons_per_row:
                col = 0
                row += 1

    # Spread the buttons evenly on the tab, centered
    def spread_buttons_horizontally(self, buttons_per_col : int = 0):
        y_offset = 10
        x_offset = 10
        if buttons_per_col == 0:
            # Calculate how many buttons can fit vertically with proper spacing
            button_height = self.__buttons[0].get_size()[1]
            available_height = self.__size[1] - (2 * y_offset)
            # Estimate spacing (use a minimum spacing value)
            min_spacing = 10
            buttons_per_col = max(1, available_height // (button_height + min_spacing))
        
        # Calculate spacing between buttons
        available_height = self.__size[1] - (2 * y_offset)
        button_height = self.__buttons[0].get_size()[1]
        button_width = self.__buttons[0].get_size()[0]
        
        # Calculate spacing to distribute buttons evenly vertically
        total_button_height = button_height * buttons_per_col
        remaining_space = available_height - total_button_height
        spacing = remaining_space // (buttons_per_col + 1)
        
        # Calculate total number of columns needed
        total_buttons = len(self.__buttons)
        num_cols = (total_buttons + buttons_per_col - 1) // buttons_per_col  # Ceiling division
        
        # Calculate total width needed for all columns
        total_width = num_cols * button_width + (num_cols - 1) * x_offset
        
        # Calculate starting x position to center horizontally
        start_x = self.__pos[0] + (self.__size[0] - total_width) // 2
        
        # Set button positions
        row = 0
        col = 0
        for button in self.__buttons:
            x_pos = start_x + col * (button_width + x_offset)
            y_pos = self.__pos[1] + y_offset + spacing + row * (button_height + spacing)
            button.change_pos((x_pos, y_pos))
            
            # Move to next row, or wrap to next column
            row += 1
            if row == buttons_per_col:
                row = 0
                col += 1

    def change_background_color(self, new_color : tuple[int, int, int, int]):
        self.__background_color = new_color

    # Create the background color surface
    def create_color_surface(self):
        self.__color_surface = pygame.Surface(self.__size, pygame.SRCALPHA)
        self.__color_surface.fill(self.__background_color)

    # Draw the tab background to the screen
    def draw_background_color(self, screen):
        if not self.__background_color:
            self.create_color_surface()

        screen.blit(self.__color_surface, self.__pos)

    def draw_tab(self, screen):
        self.draw_background_color(screen)
        for button in self.__buttons:
            button.draw(screen)

