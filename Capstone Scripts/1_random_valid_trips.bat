@ECHO OFF

REM "This script generates random valid trips"
REM "Requires Python 2.7"

SET sumo_path=C:\Users\zs633\Sumo
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET data_path=%osm_path%\data

START cmd.exe /K "%sumo_path%\tools\randomTrips.py -n %osm_path%\island.net.xml -o %data_path%\island.trips.xml -r %data_path%\island.rou.temp.xml -p 0.05 --validate --vclass="passenger" --vehicle-class="passenger" & PAUSE & EXIT 0"