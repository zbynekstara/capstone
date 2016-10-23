@ECHO OFF

REM "This script calls all the scripts at once (not the x ones)"
REM "Make sure that the additional-file line is included in Sumo config file"
REM "Requires Python 2.7"
REM "Requires matplotlib (available through Anaconda)"

SET scripts_path="C:\Users\zs633\Capstone\Capstone Scripts"

ECHO "Step 1: Random valid trips"
CALL %scripts_path%\1_random_valid_trips

ECHO "Step 2: Duarouter routes"
CALL %scripts_path%\2_duarouter_routes

ECHO "Step 3: Edge dump"
CALL %scripts_path%\3_edge_dump

ECHO "Step 4: Convert to plain format"
CALL %scripts_path%\4_convert_to_plain_format

ECHO "Step 5: Apply weights"
CALL %scripts_path%\5_apply_weights

ECHO "Step 6: Convert to gv format"
CALL %scripts_path%\6_convert_to_gv_format

ECHO "Step 7: Apply Neato"
CALL %scripts_path%\7_apply_neato

ECHO "Step 8: Convert to plain format"
CALL %scripts_path%\8_convert_to_plain_format

ECHO "Step 9: Convert to net format"
CALL %scripts_path%\9_convert_to_net_format

ECHO "Step 10: Color traffic maps"
CALL %scripts_path%\10_color_traffic_maps

ECHO All done!
EXIT 0