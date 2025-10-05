""" Base Classes """
class Doodad:
    def __init__(self, income):
        self.income = income

class Controllable(Doodad):
    def __init__(self, owner, income):
        super().__init__(income)
        self.owner = owner

class Structure(Controllable):
    def __init__(self, owner, income, sight_range, defence):
        super().__init__(owner, income)
        self.sight_range = sight_range
        self.defence = defence

class Unit(Controllable):
    def __init__(self, owner, income, sight_range, move_range, defence, attack):
        super().__init__(owner, income)
        self.sight_range = sight_range
        self.move_range = move_range
        self.defence = defence
        self.attack = attack

""" Default Structures """
class TowerTier1(Structure):
    def __init__(self, owner):
        super().__init__(owner, income = -2, sight_range = 5, defence = 2)

class TowerTier2(Structure):
    def __init__(self, owner):
        super().__init__(owner, income = -6, sight_range = 6, defence = 3)

class TownCenter(Structure):
    def __init__(self, owner):
        super().__init__(owner, income = 0, sight_range = 2, defence = 1)


class Farm(Structure):
    def __init__(self, owner, name = ""):
        super().__init__(owner, income = 6, sight_range = 1, defence = 0)
        self.name = name

""" Default Units """
class UnitTier1(Unit):
    def __init__(self, owner):
        super().__init__(owner, income = -1, sight_range = 3, move_range = 3, defence = 1, attack = 1)

class UnitTier2(Unit):
    def __init__(self, owner):
        super().__init__(owner, income = -4, sight_range = 4, move_range = 3, defence = 2, attack = 2)

class UnitTier3(Unit):
    def __init__(self, owner):
        super().__init__(owner, income = -9, sight_range = 4, move_range = 3, defence = 3, attack = 3)

class UnitTier4(Unit):
    def __init__(self, owner):
        super().__init__(owner, income = -16, sight_range = 4, move_range = 3, defence = 3, attack = 4)

