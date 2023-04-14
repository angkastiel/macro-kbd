# -*- coding: utf-8 -*-
"""
@author: kastiel
"""

import os
import io
#import time

KEY_SHIFT = 0xe1

class Commands:
    Down = 1
    Up = 2
    Press = 3
    Delay = 4
    SwitchLang = 5
    Call = 6
    WaitBtn = 7

name2key = {'CTRL': 224, 'SHIFT': 225, 'ALT': 226, 'WIN': 227, 'RCTRL': 228, 'RSHIFT': 229, 'RALT': 230, 'RWIN': 231, 'CAPSLOCK': 57, 'CAPS': 57, 'TAB': 43, 'ESC': 41, 'SPACE': 44, 'ENTER': 40, 'BACKSPACE': 42, 'BKSP': 42, 'INSERT': 73, 'INS': 73, 'DELETE': 76, 'DEL': 76, 'HOME': 74, 'END': 77, 'PAGEDOWN': 78, 'PGDN': 78, 'PAGEUP': 75, 'PGUP': 75, 'RIGHT': 79, 'LEFT': 80, 'DOWN': 81, 'UP': 82, 'F1': 58, 'F2': 59, 'F3': 60, 'F4': 61, 'F5': 62, 'F6': 63, 'F7': 64, 'F8': 65, 'F9': 66, 'F10': 67, 'F11': 68, 'F12': 69, 'SYSRQ': 70, 'PRTSCN': 70, 'SCROLLLOCK': 71, 'SCLK': 71, 'SCRLK': 71, 'BREAK': 72, 'PAUSE': 72, 'NUMLOCK': 83, 'KPSLASH': 84, 'KPASTERISK': 85, 'KPMINUS': 86, 'KPPLUS': 87, 'KPENTER': 88, 'KP1': 89, 'KP2': 90, 'KP3': 91, 'KP4': 92, 'KP5': 93, 'KP6': 94, 'KP7': 95, 'KP8': 96, 'KP9': 97, 'KP0': 98, 'KPDOT': 99, 'COMPOSE': 101, 'CMENU': 101}
cyr_langs = []
ascii_range = range(32, 127)
ascii_keys = [44, 542, 564, 544, 545, 546, 548, 52, 550, 551, 549, 558, 54, 45, 55, 56, 39, 30, 31, 32, 33, 34, 35, 36, 37, 38, 563, 51, 566, 46, 567, 568, 543, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 47, 49, 48, 547, 557, 53, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 559, 561, 560, 565]
cyr_range = range(1025, 1170)
cyr_data = [6709, 0, 0, 1588, 0, 3607, 1584, 0, 0, 0, 0, 0, 0, 2578, 0, 7689, 7734, 7687, 7704, 7695, 7703, 7731, 7699, 5637, 7700, 7701, 7694, 7705, 7708, 7693, 7690, 7691, 7686, 7697, 7688, 7684, 7727, 7706, 7707, 7692, 5650, 4656, 6678, 7696, 6708, 7735, 7709, 7177, 7222, 7175, 7192, 7183, 7191, 7219, 7187, 5125, 7188, 7189, 7182, 7193, 7196, 7181, 7178, 7179, 7174, 7185, 7176, 7172, 7215, 7194, 7195, 7180, 5138, 4144, 6166, 7184, 6196, 7223, 7197, 0, 6197, 0, 0, 1076, 0, 3095, 1072, 0, 0, 0, 0, 0, 0, 2066, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1636, 1124]
LANG_BITS = {'ua': 1024, 'by': 2048, 'ru': 4096}
KEY_MASK = 0xff | 512
SHIFT_BIT = 512
LANG_MASK = 1024 | 2048 | 4096


class ParserException(Exception):
    pass


def merge_commands(c1, c2):
    if (c1 is None):
        c1 = []
    if (c2 is None):
        c2 = []
    c1.extend(c2)
    return c1


def ascii2key(c: str):
    x = ord(c)
    if x in ascii_range:
        return ascii_keys[x - ascii_range.start]
    return 0


def cyr2key(c: str):
    x = ord(c)
    if x in cyr_range:
        return cyr_data[x - cyr_range.start]
    return 0


def press_key_cmd(r: list, k: int):
    k = k & KEY_MASK
    if k & SHIFT_BIT:
        r.append([Commands.Down, KEY_SHIFT])
        r.append([Commands.Press, k & ~SHIFT_BIT])
        r.append([Commands.Up, KEY_SHIFT])
    else:
        r.append([Commands.Press, k])


def detect_cyr_lang(keys: list):
    
    def is_cyr_str(keys: list, lbit: int):
        for x in keys:
            if (x & LANG_MASK) and not (x & lbit):
                return False
        return True
    
    for lang in cyr_langs:
        if is_cyr_str(keys, LANG_BITS[lang]):
            return lang
    return None
    

def c2k(c: str):
    k = ascii2key(c)
    return k if k != 0 else cyr2key(c)


def parse_typing(s: str):
    r = []
    cind = -1
    cyr_lang = None
    keys = list(map(c2k, s))
    #print('keys', keys)
    for k in keys:
        if k & LANG_MASK:
            cyr_lang = detect_cyr_lang(keys)
            break
    for k in keys:
        cind = cind + 1
        if k == 0:
            raise ParserException(f"Unsupported char in position {cind}, char code is {hex(ord(s[cind]))}")
        if not (k & LANG_MASK):
            press_key_cmd(r, k)
            continue
        l = cyr_lang if cyr_lang else detect_cyr_lang([k])
        if l:
            lon = 'en-' + l
            loff = l + '-en'
            prev_is_same_lang = (len(r) > 0) and (r[-1][0] == Commands.SwitchLang) and (r[-1][1] == loff)
            if prev_is_same_lang:
                r.pop() #remove switch to eng
            else:
                r.append([Commands.SwitchLang, lon])
            press_key_cmd(r, k)
            r.append([Commands.SwitchLang, loff])
            continue
        raise ParserException(f"Unsupported char in position {cind}, char code is {hex(ord(s[cind]))}")
    
    #print('r', r)
    
    prev_is_shift_up = False
    tmp = []
    for cmd in r:
        if (cmd[0] == Commands.Down) and (cmd[1] == KEY_SHIFT) and prev_is_shift_up:
            tmp.pop()
            continue
        tmp.append(cmd)
        prev_is_shift_up = (cmd[0] == Commands.Up) and (cmd[1] == KEY_SHIFT)
    r = tmp
    #print('r', r)
    return r


def parse_key(keyname: str):
    if len(keyname) == 1:
        k = ascii2key(keyname.lower())
        if (k != 0):
            return k
    if keyname.startswith('0x'):
        try:
            return int(keyname, 16)
        except Exception:
            raise ParserException(f"Cannot parse hex value '{keyname}'")
    try:
        return name2key[keyname.upper()]
    except KeyError:
        raise ParserException(f"Unknown key '{keyname}'")    
        

def parse_shortcuts(s: str):
    r = []
    s = s.replace(' +', '+').replace('+ ', '+').replace(' >', '>').replace('> ', '>')
    for part in s.split():
        i = part.find('>')
        seq = []
        if i >= 0:    
            seq = list(map(parse_key, part[i+1:].split('>')))
            part = part[0:i]
        keys = list(map(parse_key, part.split('+')))
        for k in keys:
            r.append([Commands.Down, k])
        for k in seq:
            r.append([Commands.Press, k])
        for k in list(reversed(keys)):
            r.append([Commands.Up, k])
    return r


def filename2key(s: str):
    if s.endswith('.macro'):
        s = s[0:len(s)-6]
    return int(s) if s.isdigit() else s


def parse_cmd(s: str):
    
    def p_delay(args: list):
        return [[Commands.Delay, int(args[0])]]
    
    def p_call(args: list):
        return [[Commands.Call, filename2key(args[0].lower())]]
    
    def p_waitbtn(args: list):
        return [[Commands.WaitBtn, int(args[0])]]
    
    def p_press_release(cmd, args: list):
        r = []
        for k in map(parse_key, args):
            r.append([cmd, k])
        return r
    
    l = s.split()
    if len(l) == 0:
        return []
    cmd = l[0].lower()
    args = l[1:]
    cmds = {'delay': [1, p_delay], 
            'call': [1, p_call], 
            'wait-btn': [1, p_waitbtn], 
            'press': [-1, lambda x: p_press_release(Commands.Down, x)],
            'release': [-1, lambda x: p_press_release(Commands.Up, x)],
            }
    if cmd in cmds:
        cargs = cmds[cmd][0]
        if (cargs >= 0) and (cargs != len(args)):
            raise ParserException(f"Expected {cargs} arguments for command '{cmd}'")
        else:
            if (cargs < 0) and (len(args) < abs(cargs)):
                raise ParserException(f"Expected {abs(cargs)} or more arguments for command '{cmd}'")
        try:
            return cmds[cmd][1](args)
        except ValueError as e:
            raise ParserException(str(e))
    raise ParserException(f"Unknown command '{cmd}'")


def parse_macro_file(filename: str):
    commands = None
    #t1 = time.monotonic_ns()
    f = io.open(filename, mode='r', encoding='utf-8')
    try:
        lines = f.readlines()
    finally:
        f.close()
    #t2 = time.monotonic_ns()
    #print('read file', (t2-t1)/1000000, 'ms')
    for i, line in enumerate(lines):
        r = None
        try:
            if (line is None) or (line.strip() is None) or (line.strip() == ''):
                continue
            if line.startswith('#'):
                continue
            p = line.find(':')
            if (p <= 0):
                raise ParserException("Unknown line format. Correct format: '<macro-type>:<macro>'")  
            mcr = line[0:p].lower()
            mcrdata = line[p + 1:].strip('\r\n')
            cmds = {'str':parse_typing, 'shortcut':parse_shortcuts, 'cmd':parse_cmd}
            if mcr in cmds:
                r = cmds[mcr](mcrdata)
            else:
                raise ParserException(f"Unknown macro type '{mcr}'")
        except ParserException as Err: 
            raise ParserException(f"Error in line {i}: {Err}")
        commands = merge_commands(commands, r)
    return commands


def parse_macro_dir():
    r = {}
    macro_dir = 'macro'
    files = list(sorted(os.listdir(macro_dir)))
    
    if 'ua-en.macro' in files:
        cyr_langs.append('ua')
    if 'by-en.macro' in files:
        cyr_langs.append('by')
    if 'ru-en.macro' in files:
        cyr_langs.append('ru')
        
    for i in files:
        i = i.lower()
        if i.endswith('.macro'):
            #t1 = time.monotonic_ns()
            key = filename2key(i)
            try:
                r[key] = parse_macro_file(macro_dir + '/' + i)
            except ParserException as Err:
                r[key] = {'error': str(Err)}                
            #t2 = time.monotonic_ns()
            #print(i, (t2-t1)/1000000, 'ms')
    return r

#print(parse_macro_dir())