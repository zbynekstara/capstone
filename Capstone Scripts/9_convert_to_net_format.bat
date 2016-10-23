@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET plain_path=%osm_path%\output
SET destination_path=%osm_path%\output_net

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %plain_path%\graphviz.nod.xml -e %plain_path%\graphviz.edg.xml -x %plain_path%\graphviz.con.xml -i %plain_path%\graphviz.tll.xml -o %destination_path%\graphviz.net.xml -v --ignore-errors --ignore-errors.edge-type -X "never" -W & EXIT 0"

ECHO Success!
EXIT 0