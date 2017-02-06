@ECHO OFF

REM "This script generates random valid trips"
REM "The P variable determines how many cars will be generated (default 1 => 1 per second; 0.1 => 10 per second)"

REM "Requires Python 2.7"

SET sumo_path=C:\Users\zs633\Sumo
SET map_path=%~dp00c_new_map
SET trips_path=%~dp01_trips

START /WAIT cmd.exe /K "%sumo_path%\tools\randomTrips.py -n %map_path%\test.net.xml -o %trips_path%\test.trips.xml -r %trips_path%\test.rou.temp.xml -p 0.66 --validate --vclass="passenger" --vehicle-class="passenger" & PAUSE & EXIT 0"

ECHO Success!
