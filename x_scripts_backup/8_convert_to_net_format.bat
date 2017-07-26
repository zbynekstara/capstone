@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET plain_path=%osm_path%\plain
SET output_path=%osm_path%\output
SET destination_path=%osm_path%\output_net

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %output_path%\gravity.nod.xml -e %output_path%\gravity.edg.xml -x %plain_path%\island.con.xml -i %plain_path%\island.tll.xml -o %destination_path%\gravity.net.xml -v --ignore-errors --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"

ECHO Success!