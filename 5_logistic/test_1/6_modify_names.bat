@ECHO OFF

REM "This script adds dump_speed info to all edges"

SET code_file=%~dp06_modify_names.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!