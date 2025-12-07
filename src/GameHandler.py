import pygame

import GameRenderer
import Editor
import Menu

from enum import Enum

class CurrentMenu(Enum):
    MAINMENU = 1
    LOBBY = 2
    MAPPICKER = 3
    EDITOR = 4
    GAMEPLAY = 5

# Singleton class for handling the game with its different menus and functions
class GameHandler:
    __instance = None
    __initialized = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super.__new__(cls)
        return cls.__instance

    def __init__(self):
        if not GameHandler.__initialized:
            self.__current_tab = CurrentMenu.MAINMENU

            self.__renderer = None
            self.__editor = None
            self.__menu = None

            GameHandler.__initialized = True

    def switch_menu(self, next_menu):
        self.__current_tab = next_menu

