@ECHO OFF

REM "Converts plain Sumo node and edge files with weights into gv"
REM "Also creates a modified dump file for color map drawings"

SET path="C:\Users\zs633\Capstone\Capstone Code"

START /WAIT cmd.exe /K "%path%\convert_to_gv_format.py & EXIT 0"

ECHO Success!
EXIT 0