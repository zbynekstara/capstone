@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\Zbynda\Sumo
SET osm_path=F:\Capstone\AUH\osm
SET plain_path=%osm_path%\output
SET destination_path=%osm_path%\output_net

START cmd.exe /K "netconvert -n %plain_path%\gravity.nod.xml -e %plain_path%\gravity.edg.xml -x %plain_path%\gravity.con.xml -i %plain_path%\gravity.tll.xml -o %destination_path%\gravity.net.xml -v --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"