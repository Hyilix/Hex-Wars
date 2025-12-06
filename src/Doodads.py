import random

""" Base Classes """
class Doodad:
    def __init__(self, income : int):
        self.income = income

    def get_type(self):
        return "doodad"

    def get_name(self):
        return None

    def reload_doodad(self):
        pass

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
        self.type = 0

    def get_type(self):
        return "structure"

class Unit(Controllable):
    def __init__(self, owner : int, income : int, sight_range : int, move_range : int, defence : int, attack : int):
        super().__init__(owner, income)
        self.sight_range = sight_range
        self.move_range = move_range
        self.defence = defence
        self.attack = attack
        self.type = 0

    def get_type(self):
        return "unit"

""" Default Structures """
class TowerTier1(Structure):
    def __init__(self, owner : int):
        super().__init__(owner, income = -2, sight_range = 5, defence = 2)
        self.type = 1

    def get_name(self):
        return "Tower_" + str(self.type)

class TowerTier2(Structure):
    def __init__(self, owner : int):
        super().__init__(owner, income = -6, sight_range = 6, defence = 3)
        self.type = 2

    def get_name(self):
        return "Tower_" + str(self.type)

class TownCenter(Structure):
    def __init__(self, owner : int):
        super().__init__(owner, income = 0, sight_range = 2, defence = 1)

    def get_name(self):
        return "Base"

class Farm(Structure):
    def __init__(self, owner : int, name = ""):
        super().__init__(owner, income = 6, sight_range = 1, defence = 0)
        self.name = name

    def get_name(self):
        return "Farm"

""" Default Units """
class UnitTier1(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -1, sight_range = 3, move_range = 3, defence = 1, attack = 1)
        self.type = 1

    def get_name(self):
        return "Unit_" + str(self.type)

class UnitTier2(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -4, sight_range = 4, move_range = 3, defence = 2, attack = 2)
        self.type = 2

    def get_name(self):
        return "Unit_" + str(self.type)

class UnitTier3(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -9, sight_range = 4, move_range = 3, defence = 3, attack = 3)
        self.type = 3

    def get_name(self):
        return "Unit_" + str(self.type)

class UnitTier4(Unit):
    def __init__(self, owner : int):
        super().__init__(owner, income = -16, sight_range = 4, move_range = 3, defence = 3, attack = 4)
        self.type = 4

    def get_name(self):
        return "Unit_" + str(self.type)

""" Miscellaneous """
class Tree(Doodad):
    def __init__(self):
        super().__init__(income = -1)
        self.type = random.randint(1, 2)

    def get_type(self):
        return "tree"

    def get_name(self):
        return "Tree_" + str(self.type)

class Grave(Doodad):
    def __init__(self):
        super().__init__(income = 0)
        self.type = random.randint(1, 2)

    def get_type(self):
        return "grave"

    def get_name(self):
        return "Grave_" + str(self.type)

def grave_to_tree(grave : Grave):
    del grave
    return Tree()

