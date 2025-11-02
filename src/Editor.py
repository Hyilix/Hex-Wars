import pygame

import Doodads
import HexMap
import Hex
import State
import Player

import GameRenderer
import button
import colors

class Editor():
    def __init__(self, renderer : GameRenderer.GameRenderer, map_size : tuple[int, int] = (0, 0)):
        self.renderer = renderer
        self.map_size = map_size

    def change_map_size(self, map_size : tuple[int, int]):
        self.map_size = map_size

