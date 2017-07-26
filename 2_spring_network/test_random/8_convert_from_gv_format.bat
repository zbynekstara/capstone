@ECHO OFF

REM "Converts gv file to Sumo plain files"

SET code_file=%~dp08_convert_from_gv_format.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!