@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET plain_path=%~dp04_plain
SET displaced_path=%~dp07_displaced
SET output_net_path=%~dp09_output_net

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %displaced_path%\lensing.nod.xml -e %displaced_path%\lensing.edg.xml -x %plain_path%\island.con.xml -i %plain_path%\island.tll.xml -o %output_net_path%\lensing.net.xml -v --ignore-errors --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"

ECHO Success!