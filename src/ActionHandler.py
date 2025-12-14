from collections import deque
from enum import Enum

class ActionType(Enum):
    TILE = 100
    MONEY = 200
    PLAYER = 300
    STATE = 301
    UNIT = 302

# Action class to hold an independent action
class Action:
    def __init__(self, action_type : ActionType, last_value, new_value, target, owner : object | list):
        self.__action_type = action_type
        self.__last_value = last_value
        self.__new_value = new_value

        if type(target) is str:
            if target.startswith('__') and not target.endswith('__'):
                self.__target = f'_{owner.__class__.__name__}{target}'
            else:
                self.__target = target
        else:
            self.__target = target

        self.__owner = owner

    def get_action_info(self):
        return (self.__action_type, self.__last_value, self.__new_value, self.__target, self.__owner)

    def apply_action(self):
        try:
            if self.__target == "is_central_hex":
                print(f"Apply hex central, {self.__new_value}")
            setattr(self.__owner, self.__target, self.__new_value)
        except:
            self.__owner[self.__target] = self.__new_value

    def undo_action(self):
        try:
            if self.__target == "is_central_hex":
                print(f"Undo hex central, {self.__last_value}")
            setattr(self.__owner, self.__target, self.__last_value)
        except:
            self.__owner[self.__target] = self.__last_value

# Class to hold a list of Actions
class ActionList:
    def __init__(self, actionList : list[Action]):
        self.__actions = actionList

    def add_action(self, action : Action):
        self.__actions.append(action)

    def apply_actions(self):
        tiles_actioned = []
        for action in self.__actions:
            action.apply_action()

            if action.get_action_info()[0] == ActionType.TILE:
                tiles_actioned.append(action.get_action_info()[-1])

        return tiles_actioned

    def undo_actions(self):
        tiles_actioned = []
        for action in reversed(self.__actions):
            action.undo_action()

            if action.get_action_info()[0] == ActionType.TILE:
                tiles_actioned.append(action.get_action_info()[-1])

        return tiles_actioned

    def combine_action_lists(self, other):
        for action in other.__actions:
            self.add_action(action)

    def is_list_empty(self):
        if len(self.__actions) == 0:
            return True
        return False

# Class containing ActionLists and handles the actions
class History:
    def __init__(self):
        self.__history = deque()
        self.__undo = deque()

    def __deep_clear_queue(self, queue):
        for elem in queue:
            del elem
        queue.clear()

    def deep_clear(self):
        self.__deep_clear_queue(self.__history)
        self.__deep_clear_queue(self.__undo)

    def add_action_list(self, action : ActionList):
        if action.is_list_empty() == False:
            self.__history.append(action)
            self.__deep_clear_queue(self.__undo)
            action.apply_actions()

    def extend_last_list(self, action : ActionList):
        if action.is_list_empty() == False:
            self.__history[-1].combine_action_lists(action)
            action.apply_actions()

    def undo_last_action(self):
        if self.__history:
            last_action = self.__history.pop()
            self.__undo.append(last_action)
            return last_action.undo_actions()

    def redo_last_action(self):
        if self.__undo:
            last_action = self.__undo.pop()
            self.__history.append(last_action)
            return last_action.apply_actions()


