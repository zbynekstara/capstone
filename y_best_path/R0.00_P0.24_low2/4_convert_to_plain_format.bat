@ECHO OFF

REM "This script converts Sumo net format to Sumo plain files"
REM "Those should be more readable"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET map_path=%~dp00_map
SET plain_path=%~dp04_plain

CD /D %plain_path%
START /WAIT cmd.exe /K "%sumo_path%\netconvert -s %map_path%\test.net.xml --plain-output-prefix test & PAUSE & EXIT 0"

ECHO Success!