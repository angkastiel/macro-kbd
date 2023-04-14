Macro Keyboard
==============
Supports macros for typing and keyboard shortcuts

Macros for a button should be saved to .macro file in 'macro' folder. For links macro to button, file name should be button number. For example: 1.macro, 3.macro etc.

Macro file syntax
-----------------
Each of line in macro file has structure '<macro-type>:<macro-data>'. For example 'shortcut:CTR+ALT+DEL'.

###Macro types
**str**
Used for typing. Automatically press SHIFT for uppercase letters or special characters. Space char (' ') is significant.
*Example:*
		str:Hello World! (123!?)
		 
**shortcut**
Used for press shortcuts sequences. Sequence items separated by space. For define key use key name or scan key code. Use + for shortcut.
*Examples:*
		shortcut:CTR+ALT+DEL
		shortcut:ENTER
		shortcut:CTRL+ALT+/
		
**cmd**
Used for special commands:
* ***delay*** *<ms>*
Wait <ms> miliseconds
*Example:*
		cmd:delay 150
* ***call*** *<macro_file>*
Call specified macro file
*Example:*
		cmd:call some.macro