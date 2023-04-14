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
			
### Supported key names

| Key Name | Key Scan Code | Description |
| -------- | ------------- | ----------- |
| CTRL | 0xe0 | |
| SHIFT | 0xe1 | |
| ALT | 0xe2 | |
| WIN | 0xe3 | |
| RCTRL | 0xe4 | |
| RSHIFT | 0xe5 | |
| RALT | 0xe6 | |
| RWIN | 0xe7 | |
| CAPSLOCK | 0x39 | |
| CAPS | 0x39 | |
| TAB | 0x2b | |
| ESC | 0x29 | |
| SPACE | 0x2c | |
| ENTER | 0x28 | |
| BACKSPACE | 0x2a | |
| BKSP | 0x2a | |
| INSERT | 0x49 | |
| INS | 0x49 | |
| DELETE | 0x4c | |
| DEL | 0x4c | |
| HOME | 0x4a | |
| END | 0x4d | |
| PAGEDOWN | 0x4e | |
| PGDN | 0x4e | |
| PAGEUP | 0x4b | |
| PGUP | 0x4b | |
| RIGHT | 0x4f | |
| LEFT | 0x50 | |
| DOWN | 0x51 | |
| UP | 0x52 | |
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
| SYSRQ | 0x46 | |
| PRTSCN | 0x46 | |
| SCROLLLOCK | 0x47 | |
| SKLK | 0x47 | |
| SCRLK | 0x47 | |
| BREAK | 0x48 | |
| PAUSE | 0x48 | |
| NUMLOCK | 0x53 | |
| KPSLASH | 0x54 | |
| KPASTERISK | 0x55 | |
| KPMINUS | 0x56 | |
| KPPLUS | 0x57 | |
| KPENTER | 0x58 | |
| KP1 | 0x59 | |
| KP2 | 0x5a | |
| KP3 | 0x5b | |
| KP4 | 0x5c | |
| KP5 | 0x5d | |
| KP6 | 0x5e | |
| KP7 | 0x5f | |
| KP8 | 0x60 | |
| KP9 | 0x61 | |
| KP0 | 0x62 | |
| KPDOT | 0x63 | |
| COMPOSE | 0x65 | |
| CMENU | 0x65 | |