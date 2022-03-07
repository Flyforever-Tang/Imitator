from keyboard_event import *
from mouse_event import *
from pynput import mouse, keyboard
import sys
import time
from typing import Union


class Imitator(object):
    def __init__(self,
                 ignore_mouse_repeat: bool = True,
                 ignore_keyboard_repeat: bool = True):
        self.ignore_mouse_repeat = ignore_mouse_repeat
        self.ignore_keyboard_repeat = ignore_keyboard_repeat
        self.event_list = []
        self.keep_listening = True
        self.repeating = False

    def insert_event(self,
                     event: Union[MouseEvent, KeyboardEvent]):
        if self.ignore_mouse_repeat and isinstance(event, MouseEvent):
            if isinstance(event, MouseMoveEvent) and len(self.event_list) > 0 \
                    and isinstance(self.event_list[-1], MouseMoveEvent):
                self.event_list[-1] = event
                return
        elif self.ignore_keyboard_repeat and isinstance(event, KeyboardEvent):
            if len(self.event_list) > 0 and isinstance(self.event_list[-1], KeyboardEvent):
                if event == self.event_list[-1]:
                    return
        self.event_list.append(event)

    def mouse_on_move(self,
                      x: int, y: int):
        self.insert_event(MouseMoveEvent((x, y)))
        return self.keep_listening

    def mouse_on_click(self,
                       _x: int, _y: int,
                       button: mouse.Button,
                       pressed: bool):
        self.insert_event(MousePressEvent(button, 'press' if pressed else 'release'))
        return self.keep_listening

    def mouse_on_scroll(self,
                        _x: int, _y: int,
                        dx: int, dy: int):
        self.insert_event(MouseScrollEvent((dx, dy)))
        return self.keep_listening

    def keyboard_on_press(self,
                          key: Any):
        self.insert_event(KeyboardPressEvent(key, 'press'))
        return self.keep_listening

    def keyboard_on_release(self,
                            key: Any):
        self.insert_event(KeyboardPressEvent(key, 'release'))
        return self.keep_listening

    def listen_mouse(self):
        self.event_list = []
        self.keep_listening = True
        mouse_listener = mouse.Listener(on_move=self.mouse_on_move,
                                        on_click=self.mouse_on_click,
                                        on_scroll=self.mouse_on_scroll)
        mouse_listener.start()

    def listen_keyboard(self):
        self.event_list = []
        self.keep_listening = True
        keyboard_listener = keyboard.Listener(on_press=self.keyboard_on_press,
                                              on_release=self.keyboard_on_release)
        keyboard_listener.start()

    def stop_listening(self):
        self.event_list.pop()
        self.event_list.pop()
        print(self.event_list)
        self.keep_listening = False

    def repeat(self,
               times: int,
               repeat_interval: float = 0.1,
               round_interval: float = 1):
        class KeepRepeating(object):
            flag = True

        def unexpected_move(x: int, y: int):
            if MouseMoveEvent((x, y)) not in self.event_list:
                KeepRepeating.flag = False
                return False

        KeepRepeating.flag = True
        self.repeating = True

        if times < 0:
            times = sys.maxsize

        mouse_listener = mouse.Listener(on_move=unexpected_move)
        mouse_listener.start()

        for _ in range(times):
            for event in self.event_list:
                event.reappear()
                time.sleep(repeat_interval)
            time.sleep(round_interval)
            if not KeepRepeating.flag:
                break

        self.repeating = False


if __name__ == '__main__':
    import pickle
    import PySimpleGUI as sg
    import threading

    layout = [
        [sg.Text('Repeat Times:'), sg.InputText('-1', (5, 1), key='repeat_times')],
        [sg.Text('Repeat Interval:'), sg.InputText('0.1', (5, 1), key='repeat_interval'),
         sg.Text('Round Interval:'), sg.InputText('1', (5, 1), key='round_interval')],
        [sg.Text('Ignore Mouse Repeat:'),
         sg.Radio('True', 'Ignore Mouse Repeat', True, key='ignore_mouse_repeat'),
         sg.Radio('False', 'Ignore Mouse Repeat')],
        [sg.Text('Ignore Keyboard Repeat:'),
         sg.Radio('True', 'Ignore Keyboard Repeat', True, key='ignore_keyboard_repeat'),
         sg.Radio('False', 'Ignore Keyboard Repeat')],
        [sg.Button('Start Listening'), sg.Button('Stop Listening'), sg.Button('Repeat')],
        [sg.Button('Save Operations'), sg.Button('Load Operations')]
    ]
    window = sg.Window('Imitator', layout)
    imitator = None
    while True:
        ui_event, values = window.read()
        if ui_event is None:
            break
        elif ui_event == 'Start Listening':
            if imitator is not None and imitator.repeating:
                continue
            imitator = Imitator(values['ignore_mouse_repeat'],
                                values['ignore_keyboard_repeat'])
            imitator.listen_mouse()
            imitator.listen_keyboard()
        elif ui_event == 'Stop Listening':
            if imitator is not None and not imitator.repeating:
                imitator.stop_listening()
        elif ui_event == 'Repeat':
            if imitator is not None and not imitator.repeating:
                imitator_thread = threading.Thread(target=imitator.repeat,
                                                   args=(int(values['repeat_times']),
                                                         float(values['repeat_interval']),
                                                         float(values['round_interval'])))
                imitator_thread.start()

        elif ui_event == 'Save Operations' and imitator is not None and not imitator.repeating:
            event_list = []
            for event in imitator.event_list:
                event_list.append(event)
            file_path = sg.popup_get_file('Save Operations', default_extension='.opl', save_as=True)
            if file_path != '' and file_path is not None:
                try:
                    with open(file_path, 'wb') as file:
                        pickle.dump(event_list, file)
                except BaseException as e:
                    print(e)

        elif ui_event == 'Load Operations':
            if imitator is not None and imitator.repeating:
                continue
            file_path = sg.popup_get_file('Load Operations')
            if file_path != '' and file_path is not None:
                try:
                    with open(file_path, 'rb') as file:
                        imitator = Imitator(values['ignore_mouse_repeat'],
                                            values['ignore_keyboard_repeat'])
                        imitator.event_list = pickle.load(file)
                except BaseException as e:
                    print(e)
