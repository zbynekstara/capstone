@ECHO OFF

REM "This script converts Sumo net format to Sumo plain files"
REM "Those should be more readable"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET destination_path=%osm_path%\plain

CD /D %destination_path%
START /WAIT cmd.exe /K "%sumo_path%\netconvert -s %osm_path%\island.net.xml --plain-output-prefix island & PAUSE & EXIT 0"

ECHO Success!