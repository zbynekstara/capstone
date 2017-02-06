@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET plain_path=%~dp00a_plain
SET displaced_path=%~dp00b_modified
SET output_net_path=%~dp00c_new_map

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %plain_path%\test.nod.xml -e %displaced_path%\test.edg.xml -x %plain_path%\test.con.xml -i %plain_path%\test.tll.xml -o %output_net_path%\test.net.xml -v --ignore-errors --ignore-errors.connections --ignore-errors.edge-type --remove-edges.isolated -X "never" -W & PAUSE & EXIT 0"

ECHO Success!