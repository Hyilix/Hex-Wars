from Doodads import *
import pygame

class Game:
    def __init__(self, playerCount = 1, mapSize = 10, turn = 1, round = 1):
        self.playerCount = playerCount
        self.mapSize = mapSize
        self.turn = turn
        self.round = round

    def win(self, player):
        if isinstance(player, Player):
            if (player.hexOwned >= self.mapSize * 0.7):
                print (player.playerCount + " wins")

    def rounds(self):
        if(self.turn > self.round):
            self.round = self.round + 1
            self.turn = 1

    

class Player:
    def __init__(self, hexNum = 0, income = 10, count = 1):
        self.playerCount = count
        self.income = income
        self.hexNum = hexNum
        self.units = []
        self.hexOwned = []  #should have some coordinates

    def action(self):
        pass

class HexNew:
    def __init__(self, control = None, owner = -1):
        self.owner = owner
        self.controllable = control
        self.income = 2

    def place(self, control):
        if(self.controllable == None):
            self.controllable = control
        
    def move(self, control):
        if isinstance(control, Unit) and self.controllable == Unit:
            self.controllable = None
        elif isinstance(control, Unit) and self.controllable == Unit:
            self.controllable = Unit
    
    def treeHere(self, control):
        if isinstance(control, Tree):
            self.income = 1
        else:
            self.income = 2

    