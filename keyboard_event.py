from abc import ABCMeta, abstractmethod
from pynput import keyboard
from typing import Any


class KeyboardEvent(object):
    __metaclass__ = ABCMeta
    controller = keyboard.Controller()

    def __init__(self,
                 key: Any):
        self.key = key

    @abstractmethod
    def reappear(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __eq__(self,
               other: Any):
        pass


class KeyboardPressEvent(KeyboardEvent):
    press_functions = {'press': KeyboardEvent.controller.press,
                       'release': KeyboardEvent.controller.release}

    def __init__(self,
                 key: Any,
                 press_type: str):
        super().__init__(key)
        self.press_type = press_type
        self.press_functions = KeyboardPressEvent.press_functions[press_type]

    def reappear(self):
        self.press_functions(self.key)

    def __repr__(self):
        return f'Keyboard {self.press_type} {self.key}'

    def __eq__(self,
               other: Any):
        return isinstance(other, KeyboardPressEvent) and self.key == other.key and \
               self.press_type == other.press_type
