from abc import ABCMeta, abstractmethod
import ctypes
from pynput import mouse
from typing import Tuple, Any

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


class MouseEvent(object):
    __metaclass__ = ABCMeta
    controller = mouse.Controller()

    def __init__(self,
                 coordinate: Tuple[int, int]):
        self.coordinate = coordinate

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


class MouseMoveEvent(MouseEvent):
    def __init__(self,
                 coordinate: Tuple[int, int]):
        super().__init__(coordinate)

    def reappear(self):
        MouseEvent.controller.position = self.coordinate

    def __repr__(self):
        return f'Mouse move to {self.coordinate}'

    def __eq__(self,
               other: Any):
        return isinstance(other, MouseMoveEvent) and self.coordinate == other.coordinate


class MouseClickEvent(MouseEvent):
    def __init__(self,
                 coordinate: Tuple[int, int],
                 count: int,
                 click_button: mouse.Button):
        super().__init__(coordinate)
        self.count = count
        self.click_Button = click_button

    def reappear(self):
        MouseEvent.controller.click(self.click_Button, self.count)

    def __repr__(self):
        return f'Mouse click {self.click_Button} {self.count} times at {self.coordinate}'

    def __eq__(self,
               other: Any):
        return isinstance(other, MouseClickEvent) and self.click_Button == other.click_Button and \
               self.count == other.count and self.coordinate == other.coordinate


class MousePressEvent(MouseEvent):
    press_functions = {'press': MouseEvent.controller.press,
                       'release': MouseEvent.controller.release}

    def __init__(self,
                 press_button: str,
                 press_type: str):
        super().__init__((0, 0))
        self.press_button = press_button
        self.press_type = press_type
        self.press_functions = MousePressEvent.press_functions[press_type]

    def reappear(self):
        self.press_functions(self.press_button)

    def __repr__(self):
        return f'Mouse {self.press_type} {self.press_button}'

    def __eq__(self,
               other: Any):
        return isinstance(other, MousePressEvent) and self.press_type == other.press_type and \
               self.press_button == other.press_button


class MouseScrollEvent(MouseEvent):
    def __init__(self,
                 coordinate: Tuple[int, int]):
        super().__init__(coordinate)

    def reappear(self):
        MouseEvent.controller.scroll(*self.coordinate)

    def __repr__(self):
        return f'Mouse scroll at {self.coordinate}'

    def __eq__(self,
               other: Any):
        return isinstance(other, MouseScrollEvent) and self.coordinate == other.coordinate
