@ECHO OFF

REM "This script adds dump_speed info to all edges"

SET path="C:\Users\zs633\Capstone\Capstone Code"

START /WAIT cmd.exe /K "%path%\modify_names.py & PAUSE & EXIT 0"

ECHO Success!