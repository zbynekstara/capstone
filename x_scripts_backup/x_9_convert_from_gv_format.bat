@ECHO OFF

REM "Converts gv file to Sumo plain files"

SET path="C:\Users\zs633\Capstone\Capstone Code"

START /WAIT cmd.exe /K "%path%\convert_from_gv_format.py & EXIT 0"

ECHO Success!