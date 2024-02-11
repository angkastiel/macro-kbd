import btnopt
import time
import digitalio

class Buttons:
    _list = None
    DebugButton = None
    TriggerButtons = None
    
    def __init__(self):
        self._list = []
        for pin in btnopt.buttons_pins:
            self._list.append(self._setup_btn(pin))
        self.TriggerButtons = range(len(self._list))
        self._list.append(self._setup_btn(btnopt.dbg_button_pin))
        self.DebugButton = len(self._list) - 1
            
    def _setup_btn(self, pin):
        btn = digitalio.DigitalInOut(pin)
        btn.direction = digitalio.Direction.INPUT
        btn.pull = digitalio.Pull.DOWN
        return btn
            
    def is_pressed(self, index: int):
        return bool(self._list[index].value)
    
    def get_pressed(self):
        for i, b in enumerate(self._list):
            if b.value:
                return i
        return -1
            
    def wait_pressed(self, wait_s: float, sleep_interval: float):
        time_end = time.monotonic() + wait_s
        while time.monotonic() < time_end:
            i = self.get_pressed()
            if i >= 0:
                return i
            time.sleep(sleep_interval)
        return -1
    
    def wait_click(self, wait_s: float, sleep_interval: float):
        print('wait_click: start')
        time_end = time.monotonic() + wait_s
        b = self.wait_pressed(wait_s, sleep_interval)
        print(f'wait_click: wp {b}')
        if b < 0:
            return b
        while time.monotonic() < time_end:
            if not self.is_pressed(b):
                print(f'wait_click: return {b}')
                return b
            time.sleep(0.01)
        print('wait_click: return -1')
        return -1
    
    def wait_hold(self, btn_id: int, hold_s: float):
        print('wait_hold: start')
        time_end = time.monotonic() + hold_s
        while time.monotonic() < time_end:
            if not self.is_pressed(btn_id):
                print('wait_hold: return False')
                return False
            time.sleep(0.01)
        print('wait_hold: return True')
        return True      
            