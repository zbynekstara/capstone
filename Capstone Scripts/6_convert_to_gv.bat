@ECHO OFF

REM "Converts plain Sumo node and edge files with weights into gv"

SET path="F:\Capstone\Capstone Code"

START cmd.exe /K "%path%\convert_to_gv.py & PAUSE & EXIT 0"