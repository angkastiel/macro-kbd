import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
import board
import digitalio     

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT    

led.value = True

def blink(delay, count):
    led.value = False
    time.sleep(0.02)
    for i in range(count):
        led.value = True
        time.sleep(delay)
        led.value = False
        time.sleep(delay)
    time.sleep(0.02)

def blink_no_macro():
    blink(0.05, 4)
        
def macro_start():
    if led.value:
        led.value = False
        time.sleep(0.02)
    led.value = True
    
def macro_end():
    time.sleep(0.2)
    led.value = False
    time.sleep(0.02)
    
def setup_input_btn(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN
    return btn
    
buttons_pins = [board.GP19, board.GP20, board.GP21, board.GP9, board.GP6, board.GP4, board.GP18]

buttons = []
for pin in buttons_pins:
    buttons.append(setup_input_btn(pin))

btn_dbg = setup_input_btn(board.GP15)

keyboard = Keyboard(usb_hid.devices)

from parser import parse_macro_dir
from parser import CMD_DOWN
from parser import CMD_UP
from parser import CMD_PRESS
from parser import CMD_DELAY
from parser import CMD_SWITCH_LANG
from parser import CMD_CALL
from parser import CMD_WAITBTN

trigger_button = None

def exec_down(cmd: list):
    time.sleep(0.02)
    keyboard.press(cmd[1])
    time.sleep(0.02)

def exec_up(cmd: list):
    time.sleep(0.02)
    keyboard.release(cmd[1])
    time.sleep(0.02)
    
def exec_press(cmd: list):
    keyboard.press(cmd[1])
    keyboard.release(cmd[1])
    
def exec_delay(cmd: list):
    time.sleep(cmd[1] / 1000)
    
def exec_wait_btn(cmd: list):
    if not trigger_button is None:
        fade(lambda: not trigger_button.value, cmd[1] / 1000)
    
def exec_call(cmd: list):
    if cmd[1] in macros:
        run_macro(macros[cmd[1]])
    
def run_macro(commands: list):
    cmds = {CMD_DOWN: exec_down, CMD_UP: exec_up, CMD_PRESS: exec_press, CMD_DELAY: exec_delay, CMD_CALL: exec_call, CMD_SWITCH_LANG: exec_call, CMD_WAITBTN: exec_wait_btn}
    for cmd in commands:
        cmds[cmd[0]](cmd)
                        
           
macros = parse_macro_dir()

def run_macro_for_button(key):
    if (key in macros) and (type(macros[key]) is list):
        macro_start()
        run_macro(macros[key])
        macro_end()
    else:
        blink_no_macro()
    time.sleep(0.2)

led.value = False
blink(0.03, 5)

class FadeTimeout(Exception):
    pass

def fade(while_f, timeout):
    p_start = 0
    i = 0
    reverse = False
    start = time.time()
    while (while_f()):
        t1 = time.monotonic_ns()
        if t1 - p_start > 3*1000000:
            p_start = t1
            if time.time() - start > timeout:
                if i < 5:
                    led.value = True
                    time.sleep(0.001)
                    led.value = False
                raise FadeTimeout()
            if (i == 100) or (i == -20):
                reverse = not reverse
            if not reverse:
                i = i + 1
            else:
                i = i - 1
        x = max(0, i)
        y = 100 - x
        if x:
            led.value = True
            time.sleep(x * (0.0001))
        if y:
            led.value = False
            time.sleep(y * (0.0001))

def is_dbg_pressed():
    return btn_dbg.value

while True:
    led.value = bool(btn_dbg.value)
    
    for i, btn in enumerate(buttons):
        if btn.value:
            trigger_button = btn
            try:
                run_macro_for_button(i + 1)
            except:
                pass
            finally:
                trigger_button = None
            
    time.sleep(0.1)

