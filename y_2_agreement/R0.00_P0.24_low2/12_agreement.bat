@ECHO OFF

REM "This script displaces nodes"

SET code_file=%~dp012_agreement.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!