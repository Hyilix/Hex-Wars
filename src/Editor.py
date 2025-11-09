import pygame

import Doodads
import HexMap
import Hex
import State
import Player

import GameRenderer
import button
import colors

class Tab_Editor:
    def __init__(self):
        pass

class Editor:
    def __init__(self, renderer : GameRenderer.GameRenderer, hex_map : HexMap.HexMap):
        self.renderer = renderer
        self.hex_map = hex_map

