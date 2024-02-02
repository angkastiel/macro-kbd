import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
import board
import digitalio
import btnopt
from secure import decode_str
from secure import encode_str
from secure import get_pincode_hash

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT    

led.value = True

crypotokey = None


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


buttons = []
for pin in btnopt.buttons_pins:
    buttons.append(setup_input_btn(pin))

btn_dbg = setup_input_btn(btnopt.dbg_button_pin)

keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

from parser import parse_macro_dir
from parser import parse_typing
from parser import Commands

trigger_button = None

class FadeTimeout(Exception):
    pass
class BreakMacro(Exception):
    pass

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
    
def exec_mouse_click(cmd: list):
    mouse.click(cmd[1])

def exec_mouse_down(cmd: list):
    mouse.press(cmd[1])
    
def exec_mouse_up(cmd: list):
    mouse.release(cmd[1])
    
def exec_delay(cmd: list):
    time.sleep(cmd[1] / 1000)
    
def exec_wait_br(cmd: list):
    if trigger_button is None:
        return
    try:
        fade(lambda: not trigger_button.value, cmd[1] / 1000)
        time.sleep(0.5)
        raise BreakMacro()
    except FadeTimeout:
        pass
    led.value = True
    
def exec_wait_btn(cmd: list):
    if not trigger_button is None:
        fade(lambda: not trigger_button.value, cmd[1] / 1000)
    
def exec_call(cmd: list):
    if cmd[1] in macros:
        run_macro(macros[cmd[1]])
    
def exec_repeat(cmd: list):
    while True:
        run_macro(macros[cmd[1]])
        
def exec_decode_and_type(cmd: list):
    s = decode_str(cmd[1], crypotokey)
    macro = parse_typing(s)
    run_macro(macro)
    
def exec_encode_and_type(cmd: list):
    s = encode_str(cmd[1], crypotokey)
    macro = parse_typing(s)
    run_macro(macro)
    
def run_macro(commands: list):
    cmds = {Commands.Down: exec_down, Commands.Up: exec_up, Commands.Press: exec_press, Commands.Delay: exec_delay, Commands.Call: exec_call, 
            Commands.SwitchLang: exec_call, Commands.WaitBtn: exec_wait_btn, Commands.MouseClick: exec_mouse_click,
            Commands.Repeat: exec_repeat, Commands.WaitBreak: exec_wait_br,
            Commands.MouseDown: exec_mouse_down, Commands.MouseUp: exec_mouse_up,
            Commands.DecodeAndType: exec_decode_and_type,
            Commands.EncodeAndType: exec_encode_and_type}
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
            time.sleep(x * 0.0001)
        if y:
            led.value = False
            time.sleep(y * 0.0001)


while True:
    led.value = bool(btn_dbg.value)
    
    for i, btn in enumerate(buttons):
        if btn.value:
            trigger_button = btn
            try:
                run_macro_for_button(i + 1)
            except Exception as e:
                print(e)
            finally:
                trigger_button = None
            
    time.sleep(0.1)

