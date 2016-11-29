@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET node_file=%~dp0test.nod.xml
SET edge_file=%~dp0test.edg.xml
SET output_file=%~dp0test.net.xml

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %node_file% -e %edge_file% -o %output_file% -v --no-turnarounds --ignore-errors.edge-type -X "never" -W & PAUSE & EXIT 0"

ECHO Success!