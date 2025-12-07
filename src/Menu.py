import pygame

import button
import colors
import ButtonHandler

# Super class for all the menus in the game
class Menu:
    def __init__(self, screen):
        pass

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

