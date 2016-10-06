@ECHO OFF

REM "This script generates duarouter routes"
REM "Uses free-flow situation to inform routing"
REM "According to Jerome, this is the most realistic looking one"
REM "Apart from the Corniche, which should have more traffic"
REM "Requires Python 2.7"

SET sumo_path=C:\Users\Zbynda\Sumo
SET osm_path=F:\Capstone\AUH\osm
SET data_path=%osm_path%\data
SET destination_path=%osm_path%\duarouter

START cmd.exe /K "duarouter -n %osm_path%\island.net.xml -t %data_path%\island.trips.xml -o %destination_path%\island.rou.xml --ignore-errors -b 0 -e 3600 --no-step-log --no-warnings & PAUSE & EXIT 0"