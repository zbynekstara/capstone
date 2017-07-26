@ECHO OFF

REM "This script adds dump_speed info to all edges"

SET code_file=%~dp05_apply_weights.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!