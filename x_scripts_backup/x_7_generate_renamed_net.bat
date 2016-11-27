@ECHO OFF

REM "This script takes modifed node and edge files and puts them into a net."
REM "This way the original map has the new labels."

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET modified_path=%osm_path%\output
SET plain_path=%osm_path%\plain
SET destination_path=%osm_path%

START cmd.exe /K "%sumo_path%\netconvert -n %modified_path%\modified.nod.xml -e %modified_path%\modified.edg.xml -x %plain_path%\island.con.xml -i %plain_path%\island.tll.xml -o %destination_path%\modified.net.xml -v --ignore-errors --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"