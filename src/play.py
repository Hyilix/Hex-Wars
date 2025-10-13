from Doodads import *
import pygame
from Player import *

class Game:
    def __init__(self, playerCount = 1, mapSize = 10, turn = 1, round = 1):
        self.playerCount = playerCount
        self.mapSize = mapSize
        self.turn = turn
        self.round = round

    def win(self, player):
        if isinstance(player, Player):
                print (player.owner + " wins")

    

    def next_turn(self):
        pass
    
class HexNew(Hex):
    def __init__(self,  x_pos : int, y_pos : int, control = None, owner = -1):
        self.position = (x_pos, y_pos)
        self.owner = owner
        self.controllable = control
        self.income = 2

    def place(self, control):
        if(self.controllable == None):
            self.controllable = control
        
    def move(self, control):
        if isinstance(control, Unit) and self.controllable == Unit:
            self.controllable = None
        elif isinstance(control, Unit) and self.controllable == None:
            self.controllable = control
            control.moved = 1
    
    # def treeHere(self, control):
    #     if isinstance(control, Tree):
    #         self.income = 1
    #     else:
    #         self.income = 2

    