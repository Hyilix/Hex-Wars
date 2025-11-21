from collections import deque
from enum import Enum

class ActionType(Enum):
    TILE = 100
    MONEY = 200

class Action:
    def __init__(self, action_type : ActionType, last_value, new_value, target : str, owner : object):
        self.__action_type = action_type
        self.__last_value = last_value
        self.__new_value = new_value

        if target.startswith('__') and not target.endswith('__'):
            self.__target = f'_{owner.__class__.__name__}{target}'
        else:
            self.__target = target

        self.__owner = owner

    def get_action_info(self):
        return (self.__action_type, self.__last_value, self.__new_value, self.__target, self.__owner)

    def apply_action(self):
        setattr(self.__owner, self.__target, self.__new_value)

    def undo_action(self):
        setattr(self.__owner, self.__target, self.__last_value)

class ActionList:
    def __init__(self, ):
        self.__actions = deque()

class History:
    def __init__(self):
        self.__history = deque()
        self.__undo = deque()

    def __deep_clear_queue(self, queue):
        for elem in queue:
            del elem
            queue.pop()

    def add_action(self, action : ActionList):
        self.__history.append(action)
        self.__deep_clear_queue(self.__undo)
        # TODO: Handle action

    def undo_action_last(self):
        last_action = self.__history.pop()
        self.__undo.append(last_action)
        # TODO: undo last action in world

    def redo_last_action(self):
        last_action = self.__undo.pop()
        self.__history.append(last_action)
        # TODO: handle action


