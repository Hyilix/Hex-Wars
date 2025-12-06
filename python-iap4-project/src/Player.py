from State import State
import Hex
from Doodads import *
import HexMap

from HexMap import *
from play import HexNew

class Player:
    def __init__(self, hexNum: int, income : int, owner : int, color : tuple[int, int, int]):
        self.owner = owner
        self.color = color

        # self.income = income
        self.hexNum = hexNum
        self.units = [Unit]
        self.states: list[State] = []

    def change_color(self, new_color : tuple[int, int, int]):
        self.color = new_color

    def get_states(self):
        return self.states

    def add_state(self, state : State):
        self.states.append(state)
        pass
        


    def move(self, hexs : Hex, hexd : Hex, searchHex : HexMap): # s = source, d = destination 
        if isinstance(hexs.doodad,  Unit):
            if (abs(hexs.position[0] - hexd.position[0]) + 
                abs(hexs.position[1] - hexd.position[1]) <= hexs.doodad.move_range
                and hexd.owner == hexs.owner):
                
                if (hexd.doodad == None):
                    hexd.doodad = hexs.doodad
                    hexs.doodad = None
                
                elif isinstance(hexd.doodad, Unit):
                    merged = hexd.doodad.mergeUnit(hexs.doodad, hexs.owner)
                    if (merged != None):
                        hexd.doodad = merged
                        hexs.doodad = None
                    else: pass
                else: pass
            elif (abs(hexs.position[0] - hexd.position[0]) + 
                abs(hexs.position[1] - hexd.position[1]) <= hexs.doodad.move_range and 
                hexd.owner != hexs.owner and hexd.owner != -1):
                
                neigh = searchHex.get_hex_all_neighbors(hexd)
                for n in neigh:
                    for s in self.states:
                        if n is not None and s.is_hex_in_estate(n) : #can move there
                            if ((hexd.doodad == None or hexd.doodad == Farm) or 
                                isinstance(hexd.doodad, Unit) and isinstance(hexs.doodad, Unit) and
                                ((hexd.doodad.attack < hexs.doodad.attack) 
                                or (hexd.doodad == TownCenter and hexs.doodad.attack > 1) 
                                or (hexd.doodad == TowerTier1 and hexs.doodad.attack > 2)
                                or (hexd.doodad == TowerTier2 and hexs.doodad.attack > 3))):

                                
                                hexd.owner = hexs.owner
                                hexd.doodad = hexs.doodad
                                hexs.doodad = None

                            break
                # if (searchHex.get_hex_all_neighbors(hexd)).
        
        else : pass
        