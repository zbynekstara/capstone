@ECHO OFF

REM "This script removes edges"

SET code_file=%~dp00b_remove_edges.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!