@ECHO OFF

REM "This script generates duaIterate routes"
REM "Iterate through duarouter to progressively perfect the routes"
REM "Requires Python 2.7"

SET sumo_path=C:\Users\Zbynda\Sumo
SET osm_path=F:\Capstone\AUH\osm
SET data_path=%osm_path%\data
SET destination_path=%osm_path%\duaiterate

CD /D %destination_path%
START cmd.exe /K "%sumo_path%\tools\assign\duaIterate.py -n %osm_path%\island.net.xml -t %data_path%\island.trips.xml -b 0 -e 3600 & PAUSE & EXIT 0"