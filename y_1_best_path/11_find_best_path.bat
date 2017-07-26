@ECHO OFF

REM "This script displaces nodes"

SET code_file=%~dp011_find_best_path.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!