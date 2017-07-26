@ECHO OFF

REM "This script displaces nodes"

SET path="C:\Users\zs633\Capstone\Capstone Code"

START /WAIT cmd.exe /K "%path%\displace_nodes.py & PAUSE & EXIT 0"

ECHO Success!