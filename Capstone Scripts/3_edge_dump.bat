@ECHO OFF

REM "Makes sure additional-file is modified"
REM ECHO Did you add the edgeData line into the additional file?

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET data_path=%osm_path%\duarouter
REM SET destination_path=%osm_path%\duarouter

REM START /WAIT cmd.exe /K "%sumo_path%\sumo -c %data_path%\island.sumocfg & EXIT 0"
START /WAIT cmd.exe /K "%sumo_path%\sumo -n %osm_path%\island.net.xml -r %data_path%\island.rou.xml -a %data_path%\island.add.xml -b 0 -e 3600 --routing-algorithm astar -v -W & EXIT 0"

ECHO Success!
EXIT 0