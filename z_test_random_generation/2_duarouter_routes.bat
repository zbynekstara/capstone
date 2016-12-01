@ECHO OFF

REM "This script generates duarouter routes"
REM "Uses free-flow situation to inform routing"
REM "According to Jerome, this is the most realistic looking one"
REM "Apart from the Corniche, which should have more traffic"

REM "Requires Python 2.7"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET map_path=%~dp00_map
SET trips_path=%~dp01_trips
SET routes_path=%~dp02_routes

START /WAIT cmd.exe /K "%sumo_path%\duarouter -n %map_path%\test.net.xml -t %trips_path%\test.trips.xml -o %routes_path%\test.rou.xml --ignore-errors -b 0 -e 3600 --no-step-log --no-warnings & PAUSE & EXIT 0"

ECHO Success!