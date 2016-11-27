@ECHO OFF

REM "Runs Sumo to create an edge dump file"
REM "Make sure to add an appropriate .add file!"
REM "The .add file should refer to this address: .\..\3_dump\island.dump.xml"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET map_path=%~dp00_map
SET routes_path=%~dp02_routes
SET add_path=%~dp02x_add

START /WAIT cmd.exe /K "%sumo_path%\sumo -n %map_path%\island.net.xml -r %routes_path%\island.rou.xml -a %add_path%\island.add.xml -b 0 -e 3600 --routing-algorithm astar -v -W & PAUSE & EXIT 0"

ECHO Success!