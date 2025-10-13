from State import State
import Hex
from Doodads import *
import HexMap
from play import HexNew
from HexMap import *

class Player:
    def __init__(self, hexNum: int, income : int, owner : int, color : tuple[int, int, int]):
        self.owner = owner
        self.color = color

        self.income = income
        self.hexNum = hexNum
        self.units = [Unit]
        self.states = [Hex]

    def change_color(self, new_color : tuple[int, int, int]):
        self.color = new_color

    def get_states(self):
        return self.states

    def add_state(self, state : State):
        self.states.append(state)

    def move(self, hexs : HexNew, hexd : HexNew): # s = source, d = destination 
        if isinstance(hexs.controllable, Unit):
            if (abs(hexs.position[0] - hexd.position[0]) + 
                abs(hexs.position[1] - hexd.position[1]) <= hexs.controllable.move_range 
                and hexd.owner == hexs.owner):
                
                if (hexd.controllable == None):
                    hexd.controllable = hexs.controllable
                    hexs.controllable = None
                
                elif isinstance(hexd.controllable, Unit):
                    merged = hexd.controllable.mergeUnit(hexs.controllable)
                    if (merged != None):
                        hexd.controllable = merged
                        hexs.controllable = None
                    else: pass
                else: pass
            elif (abs(hexs.position[0] - hexd.position[0]) + 
                abs(hexs.position[1] - hexd.position[1]) <= hexs.controllable.move_range and 
                hexd.owner != hexs.owner and hexd.owner != -1):
                
                searchHex = HexMap
                neigh = searchHex.get_hex_all_neighbors(hexd)
                for n in neigh:
                    for s in self.states:
                        if (s.get_position == n): #can move there
                            if (hexd.controllable == None or hexd.controllable == Farm) or (hexd.controllable.attack < hexs.controllable.attack) or (hexd.controllable == TownCenter and hexs.controllable.attack > 1) or (hexd.controllable == TowerTier1 and hexs.controllable.attack > 2) or (hexd.controllable == TowerTier2 and hexs.controllable.attack > 3):
                                hexd.owner = hexs.owner
                                hexd.controllable = hexs.controllable
                                hexs.controllable = None

                            break
                # if (searchHex.get_hex_all_neighbors(hexd)).
        
        else : pass
    
    def capture(self):
        pass