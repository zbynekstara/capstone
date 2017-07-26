@ECHO OFF

REM "This script converts Sumo plain files to Sumo net format"
REM "Min speed of 13 mps is for 50 kph/30 mph and above"
REM "Min speed of 15 mps is for 60 kph/35 mph and above - THE BEST"
REM "Min speed of 18 mps is for 70 kph/40 mph and above"
REM "Min speed of 22 mps is for 80 kph/50 mph and above"
REM "Min speed of 26 mps is for 90 kph/60 mph and above"

SET sumo_path=C:\Users\zs633\Sumo\bin
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET plain_path=%osm_path%\plain
SET output_path=%osm_path%\output
SET destination_path=%osm_path%\simplified_net

START /WAIT cmd.exe /K "%sumo_path%\netconvert -n %output_path%\modified.nod.xml -e %output_path%\modified.edg.xml -x %plain_path%\island.con.xml -i %plain_path%\island.tll.xml -o %destination_path%\modified.net.xml -v --ignore-errors true --keep-edges.min-speed 15.0 --ignore-errors.edge-type true --remove-edges.isolated true -X "never" -W & PAUSE & EXIT 0"

ECHO Success!