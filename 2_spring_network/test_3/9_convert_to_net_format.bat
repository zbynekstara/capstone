@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET processed_path=%~dp08_processed
SET output_net_path=%~dp09_output_net

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %processed_path%\graphviz.nod.xml -e %processed_path%\graphviz.edg.xml -x %processed_path%\graphviz.con.xml -i %processed_path%\graphviz.tll.xml -o %output_net_path%\graphviz.net.xml -v --ignore-errors --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"

ECHO Success!