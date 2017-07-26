@ECHO OFF

REM "This script displaces nodes"

SET code_file=%~dp07_displace_nodes.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!