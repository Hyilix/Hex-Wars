import pygame

import GameRenderer
import Hex
import HexMap
import Player

import button
import utils
import Events

import MapHandling

import ActionHandler
import KeyboardState
import ButtonHandler

class Gameplay:
    def __init__(self, renderer : GameRenderer.GameRenderer, hex_map : HexMap.HexMap, screen_size : tuple[int, int]):
        self.__renderer = renderer
        self.__hex_map = hex_map

        self.__screen_size = screen_size

        self.__players = [None, None, None, None, None, None]
        self.__current_player = 0

        self.__config = {
                "Hash": 0,
                "Name": "",
                "Players": self.__players,
                "CurrentPlayer": self.__current_player,
                "Map": self.__hex_map
                }

        self.action_handler = ActionHandler.History()

    # Load a game and save the game configuration
    def load_game(self, game_name):
        config = MapHandling.load_map(game_name)
        if config != None:
            self.__config = config

            self.__hex_map = self.__config.get("Map")
            self.__renderer.reload_renderer(self.__hex_map)

            self.__players = self.__config.get("Players")

            self.action_handler.deep_clear()

            pygame.event.post(pygame.event.Event(Events.MAP_CHANGED))

