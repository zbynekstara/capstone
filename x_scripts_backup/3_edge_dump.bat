@ECHO OFF

REM "Runs Sumo to create an edge dump file

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET data_path=%osm_path%\duarouter
REM SET destination_path=%osm_path%\duarouter

START /WAIT cmd.exe /K "%sumo_path%\sumo -n %osm_path%\island.net.xml -r %data_path%\island.rou.xml -a %data_path%\island.add.xml -b 0 -e 3600 --routing-algorithm astar -v -W & PAUSE & EXIT 0"

ECHO Success!