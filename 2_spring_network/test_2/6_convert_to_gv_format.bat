@ECHO OFF

REM "Converts plain Sumo node and edge files with weights into gv"
REM "Also creates a modified dump file for color map drawings"

SET code_file=%~dp06_convert_to_gv_format.py

START /WAIT cmd.exe /K "%code_file% & PAUSE & EXIT 0"

ECHO Success!