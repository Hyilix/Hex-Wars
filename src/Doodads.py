""" Base Classes """
class Doodad:
    def __init__(self, income : int):
        self.income = income

# NOTE:
# Owner convention:
#  -1 ->  tile not existing
#   0 ->  tile neutral
# 1-8 ->  tile controlled by player 1-8
# The number of max players is not yet defined, 8 is taken as just an example

class Controllable(Doodad):
    def __init__(self, owner : int, income : int):
        super().__init__(income)
        self.owner = owner

class Structure(Controllable):
    def __init__(self, owner : int, income : int, sight_range : int, defence : int):
        super().__init__(owner, income)
        self.sight_range = sight_range
        self.defence = defence

class Unit(Controllable):
    def __init__(self, owner : int, income : int, sight_range : int, move_range : int, defence : int, attack : int):
        super().__init__(owner, income)
        self.sight_range = sight_range
        self.move_range = move_range
        self.defence = defence
        self.attack = attack

    def mergeUnit(self, unit_b: "Unit"):
        a = self.attack + unit_b.attack
        if (a == 2):
            return UnitTier2
        elif (a == 3):
            return UnitTier3
        elif (a == 4):
            return UnitTier4
        else: 
            return None
""" Default Structures """
class TowerTier1(Structure):
    def __init__(self, owner : int):
        super().__init__(owner, income = -2, sight_range = 5, defence = 2)

class TowerTier2(Structure):
    def __init__(self, owner : int):
        super().__init__(owner, income = -6, sight_range = 6, defence = 3)

class TownCenter(Structure):
    def __init__(self, owner : int):
        super().__init__(owner, income = 0, sight_range = 2, defence = 1)

class Farm(Structure):
    def __init__(self, owner : int, name = ""):
        super().__init__(owner, income = 6, sight_range = 1, defence = 0)
        self.name = name

""" Default Units """
class UnitTier1(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -1, sight_range = 3, move_range = 3, defence = 1, attack = 1)

class UnitTier2(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -4, sight_range = 4, move_range = 3, defence = 2, attack = 2)

class UnitTier3(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -9, sight_range = 4, move_range = 3, defence = 3, attack = 3)

class UnitTier4(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -16, sight_range = 4, move_range = 3, defence = 3, attack = 4)

