@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET plain_path=%osm_path%\output
SET destination_path=%osm_path%\output_net

START cmd.exe /K "netconvert -n %plain_path%\graphviz.nod.xml -e %plain_path%\graphviz.edg.xml -x %plain_path%\graphviz.con.xml -i %plain_path%\graphviz.tll.xml -o %destination_path%\graphviz.net.xml -v --ignore-errors --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"