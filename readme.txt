Macros for button need save to *.macro file in 'macro' folder. File name is button number: 1.macro, 3.macro etc. Macro file contains several lines. Each of line has structure '<macro-type>:<macro-data>'. For examle 'shortcut:CTR+ALT+DEL'.

Supported macro types:
   str
      Used for typing text. Automatically press SHIFT for uppercase letters or special characters. Space char (' ') is significant.
      example:
         str:Hello World! (123!@#)
   shortcut
      Used for press shortcuts sequences. Sequence items separated by space. For define key use key name or scan key code. Use + for shortcut.
      example:
         shortcut:CTR+ALT+DEL
         shortcut:ENTER
         shortcut:CTRL+ALT+/
   cmd
      Used for special commands.
	  Supported commands:
         delay <ms>
            Wait <ms> miliseconds
            example:
               cmd:delay 150
         call <macro_file>
            Call specified macro file
			example:
			   cmd:call ru-en.macro