@ECHO OFF

REM "This script converts Sumo net format to Sumo plain files"
REM "Those should be more readable"

SET sumo_path=C:\Users\Zbynda\Sumo
SET osm_path=F:\Capstone\AUH\osm
SET destination_path=%osm_path%\plain

CD /D %destination_path%
START cmd.exe /K "netconvert -s %osm_path%\island.net.xml --plain-output-prefix island & PAUSE & EXIT 0"