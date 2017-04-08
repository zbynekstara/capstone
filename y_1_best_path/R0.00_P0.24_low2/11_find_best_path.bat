@ECHO OFF

REM "This script displaces nodes"

SET code_file=%~dp011_find_best_path.py

SET /P start_node="Start node: "
SET /P target_node="Target node: "
SET /P supplied_path="Supplied path (or None): "

START /WAIT cmd.exe /K "%code_file% %start_node% %target_node% %supplied_path% & PAUSE & EXIT 0"

ECHO Success!