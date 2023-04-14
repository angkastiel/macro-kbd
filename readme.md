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