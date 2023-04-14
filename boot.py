import storage
import board
import digitalio 
import time

btn_dbg_pin = board.GP15

btn_dbg = digitalio.DigitalInOut(btn_dbg_pin)
btn_dbg.direction = digitalio.Direction.INPUT
btn_dbg.pull = digitalio.Pull.DOWN

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

if not btn_dbg.value:
    led.value = True
    try:
        errors = []
        from parser import parse_macro_dir
        t1 = time.monotonic_ns()
        macro = parse_macro_dir()
        t2 = time.monotonic_ns()
        t = (t2 - t1) / 1000000
        #raise Exception(f"parse_macro_dir {t} ms")
        for i, (k, v) in enumerate(macro.items()):
            if type(v) is dict:
                if 'error' in v:
                    errors.append('Error in macro file ' + str(k) + '.macro: ' + str(v['error']))
        if len(errors) > 0:
            raise Exception("\n".join(errors))
        storage.disable_usb_drive()
    finally:
        led.value = False