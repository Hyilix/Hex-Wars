import pygame

import Doodads
import HexMap
import Hex
import State
import Player
import GameRenderer
import MapHandling
import button
import colors

class Editor:
    def __init__(self, renderer : GameRenderer.GameRenderer, hex_map : HexMap.HexMap):
        self.__renderer = renderer
        self.__hex_map = hex_map

        self.__config = {
                "Hash": 0,
                "Name": "New_Map",
                "Players": [],
                "CurrentPlayer": 0,
                "Map": self.__hex_map
                }

    # Load a game and save the game configuration
    def load_game(self, game_name : str):
        config = MapHandling.load_game(game_name)
        self.__config = config
        self.__renderer.reload_renderer(self.__hex_map)

    # Save the current game
    def save_game(self, game_name : str):
        MapHandling.save_game(self.__config, game_name)
