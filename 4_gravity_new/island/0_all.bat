@ECHO OFF

REM "This script calls all the scripts one after another (not the x ones)"
REM "Make sure that the additional-file line is included in Sumo config file"
REM "Requires Python 2.7 and matplotlib (available through Anaconda)"

SET scripts_path="C:\Users\zs633\Capstone\Capstone Scripts"

ECHO Executing capstone scripts

ECHO Step 1: Random valid trips
ECHO %DATE% %TIME%
CALL %scripts_path%\1_random_valid_trips

ECHO Step 2: Duarouter routes
ECHO %DATE% %TIME%
CALL %scripts_path%\2_duarouter_routes

ECHO Step 3: Edge dump
ECHO %DATE% %TIME%
CALL %scripts_path%\3_edge_dump

ECHO Step 4: Convert to plain format
ECHO %DATE% %TIME%
CALL %scripts_path%\4_convert_to_plain_format

ECHO Step 5: Apply weights
ECHO %DATE% %TIME%
CALL %scripts_path%\5_apply_weights

ECHO Step 6: Modify names
ECHO %DATE% %TIME%
CALL %scripts_path%\6_modify_names

ECHO Step 7: Convert to gv format
ECHO %DATE% %TIME%
CALL %scripts_path%\7_convert_to_gv_format

ECHO Step 8: Apply Neato
ECHO %DATE% %TIME%
CALL %scripts_path%\8_apply_neato

ECHO Step 9: Convert from gv format
ECHO %DATE% %TIME%
CALL %scripts_path%\9_convert_from_gv_format

ECHO Step 10: Convert to net format
ECHO %DATE% %TIME%
CALL %scripts_path%\10_convert_to_net_format

ECHO Step 11: Color traffic maps
ECHO %DATE% %TIME%
CALL %scripts_path%\11_color_traffic_maps

ECHO All done!
ECHO %DATE% %TIME%
PAUSE
EXIT 0