from buttons import Buttons
import time

class PincodeInput:
    _buttons = None
    
    def __init__(self, buttons: Buttons):
        self._buttons = buttons
    
    def enter_pin(self, on_enter_digit):
        r = bytearray(0)
        time_end = time.monotonic() + 5.0
        while time.monotonic() < time_end:
            btn = self._buttons.wait_click(5.0, 0.1)
            time_end = time.monotonic() + 5.0
            if not (btn in self._buttons.TriggerButtons):
                return r
            on_enter_digit()
            r = r + int(btn).to_bytes(1, 'big')
            time.sleep(0.1)