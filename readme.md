# Macro Keyboard

Supports macros for typing and keyboard shortcuts.

Macros for a button should be saved to .macro file in 'macro' folder. For links macro to button, file name should be button number. For example: 1.macro, 3.macro etc.

## Macro file syntax

Each of line in macro file has structure *'&lt;macro-type&gt;:&lt;macro-data&gt;'*. Line starts with '#' is comment.

*Examples:*

		#next line type AbcD
		str:AbcD
		#next line press CTR+ALT+DEL
		shortcut:CTR+ALT+DEL

### Macro types

* **str** - used for typing. Automatically press SHIFT for uppercase letters or special characters. Space char (' ') is significant.

*Examples:*

		str:Hello World!
		str:123$*!.({[]})
		 
* **shortcut** - used for press shortcuts sequences. Sequence items separated by space. For define key use key name or scan key code (hex value). Use + for press several keys. Use &gt; for press and release key.

*Examples:*

		#press and release ENTER
		shortcut:ENTER
		#press and release key with code 0xe1
		shortcut:0xe1
		#press and release A
		shortcut:A
		#press and release ENTER, press and release TAB
		shortcut:ENTER TAB
		#press CTRL, press ALT, press DEL, release DEL, release ALT, release CTRL
		shortcut:CTR+ALT+DEL
		#press CTRL, press SHIFT, press and release LEFT, press and release LEFT, release SHIFT, release CTRL
		shortcut:CTRL+SHIFT>LEFT>LEFT
		
* **cmd** - used for special commands:

    - ***delay*** *&lt;ms&gt;* - wait &lt;ms&gt; miliseconds before continue macro execution.
    
        *Examples:*

    		cmd:delay 150
    		cmd:delay 1200
		
    * ***call*** *&lt;macro_file&gt;* - execute specified macro file.

        *Examples:*

    		cmd:call some.macro
    		cmd:call 1.macro
    		
    * ***wait-btn*** *&lt;timeout_ms&gt;* - wait for press button that triggered the macro for &lt;timeout_ms&gt; ms. If button is not pressed until time is out macro execution will be break.

        *Examples:*

    		cmd:wait-btn 5000
    		cmd:wait-btn 1000
    		
    * ***press*** *&lt;key_definition&gt;* - press specified key.

        *Examples:*

    		cmd:press CTRL
    		cmd:press 9
    		cmd:press A
    		cmd:press [
    		cmd:press 0xe1
    		
    * ***release*** *&lt;key_definition&gt;* - release specified key.

        *Examples:*

    		cmd:release CTRL
    		cmd:release 9
    		cmd:release A
    		cmd:release [
    		cmd:release 0xe1
			
    * ***repeat*** *&lt;macro_file&gt;* - repeat specified macro file.

        *Examples:*

    		cmd:repeat some.macro
    		cmd:repeat 1.macro
    		
    * ***wait-break*** *&lt;timeout_ms&gt;* - wait for press button that triggered the macro for &lt;timeout_ms&gt; ms. If button is pressed until time is out macro execution will be break.

        *Examples:*

    		cmd:wait-break 5000
    		cmd:wait-break 1000
			
    * ***mouse-down*** *&lt;mouse_button_definition&gt;* - press specified mouse button.

        *Examples:*

    		cmd:mouse-down LEFT
    		cmd:mouse-down RIGHT
    		cmd:mouse-down MIDDLE
    		
    * ***mouse-up*** *&lt;mouse_button_definition&gt;* - release specified mouse button.

        *Examples:*

    		cmd:mouse-up LEFT
    		cmd:mouse-up RIGHT
    		cmd:mouse-up MIDDLE
			
    * ***mouse-click*** *&lt;mouse_button_definition&gt;* - press and release (click) specified mouse button.

        *Examples:*

    		cmd:mouse-click LEFT
    		cmd:mouse-click RIGHT
    		cmd:mouse-click MIDDLE
			
### Supported key names

| Key Name | Key Scan Code | Description |
| -------- | ------------- | ----------- |
| CTRL | 0xe0 | |
| SHIFT | 0xe1 | |
| ALT | 0xe2 | |
| WIN | 0xe3 | Windows key |
| RCTRL | 0xe4 | Right CTRL |
| RSHIFT | 0xe5 | Right SHIFT |
| RALT | 0xe6 | Right Alt |
| RWIN | 0xe7 | Right Windows|
| CAPSLOCK | 0x39 | |
| CAPS | 0x39 | Equal to CAPSLOCK |
| TAB | 0x2b | |
| ESC | 0x29 | |
| SPACE | 0x2c | |
| ENTER | 0x28 | |
| BACKSPACE | 0x2a | |
| BKSP | 0x2a | Equal to BACKSPACE |
| INSERT | 0x49 | |
| INS | 0x49 | Equal to INSERT |
| DELETE | 0x4c | |
| DEL | 0x4c | Equal to DELETE |
| HOME | 0x4a | |
| END | 0x4d | |
| PAGEDOWN | 0x4e | |
| PGDN | 0x4e | Equal to PAGEDOWN |
| PAGEUP | 0x4b | |
| PGUP | 0x4b | Equal to PAGEUP |
| RIGHT | 0x4f | Right arrow |
| LEFT | 0x50 | Left arrow |
| DOWN | 0x51 | Down arrow |
| UP | 0x52 | Up arrow |
| F1 | 0x3a | |
| F2 | 0x3b | |
| F3 | 0x3c | |
| F4 | 0x3d | |
| F5 | 0x3e | |
| F6 | 0x3f | |
| F7 | 0x40 | |
| F8 | 0x41 | |
| F9 | 0x42 | |
| F10 | 0x43 | |
| F11 | 0x44 | |
| F12 | 0x45 | |
| SYSRQ | 0x46 | SysRq/Print Screen key |
| PRTSCN | 0x46 | SysRq/Print Screen key |
| SCROLLLOCK | 0x47 | |
| SCLK | 0x47 | Equal to SCROLLLOCK |
| SCRLK | 0x47 | Equal to SCROLLLOCK |
| BREAK | 0x48 | Pause/Break key |
| PAUSE | 0x48 | Pause/Break key |
| NUMLOCK | 0x53 | |
| KPSLASH | 0x54 | Numpad / |
| KPASTERISK | 0x55 | Numpad * |
| KPMINUS | 0x56 | Numpad - |
| KPPLUS | 0x57 | Numpad + |
| KPENTER | 0x58 | Numpad ENTER |
| KP1 | 0x59 | Numpad 1 |
| KP2 | 0x5a | Numpad 2 |
| KP3 | 0x5b | Numpad 3 |
| KP4 | 0x5c | Numpad 4 |
| KP5 | 0x5d | Numpad 5 |
| KP6 | 0x5e | Numpad 6 |
| KP7 | 0x5f | Numpad 7 |
| KP8 | 0x60 | Numpad 8 |
| KP9 | 0x61 | Numpad 9 |
| KP0 | 0x62 | Numpad 0 |
| KPDOT | 0x63 | Numpad . |
| COMPOSE | 0x65 | Context menu key |
| CMENU | 0x65 | Context menu key |