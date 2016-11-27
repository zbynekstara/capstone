@ECHO OFF

REM "This script generates one-shot routes"
REM "DUA only once at time specified by f"
REM "Works pretty well apparently"
REM "Requires Python 2.7"

SET sumo_path=C:\Users\Zbynda\Sumo
SET osm_path=F:\Capstone\AUH\osm
SET data_path=%osm_path%\data
SET destination_path=%osm_path%\one_shot

CD /D %destination_path%
START cmd.exe /K "%sumo_path%\tools\assign\one-shot.py -f 900 -n %osm_path%\island.net.xml -t %data_path%\island.trips.xml -b 0 -e 3600 -L -s & PAUSE & EXIT 0"