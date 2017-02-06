@ECHO OFF

REM "This script generates traffic color maps"

REM "Requires Python 2.7 and matplotlib (available through Anaconda)"

REM "This can be run after step 6"

REM "Google colormap: 65-50/65 = green, 50-30/65 = orange, 30-5/65 = red, 5-0/65 = dark red"
REM "In terms of slowdown_ratio: 0.00-0.23, 0.23-0.54, 0.54-0.92, 0.92-1.00"

SET sumo_path=C:\Users\zs633\Sumo
SET map_path=%~dp00c_new_map
SET dump_path=%~dp06_prepared
SET output_path=%~dp010c_google_map

START /WAIT cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %map_path%\test.net.xml -i %dump_path%\modified.dump.xml,%dump_path%\modified.dump.xml -o %output_path%\google.colormap.png -m slowdown_ratio,entered --default-color #808080 --default-width 2.0 --min-color-value 0.0 --max-color-value 1.0 --min-width-value 0.0 --max-width-value 100.0 --colormap #0:#00cc00,0.229999:#00cc00,0.23:#ff6600,0.539999:#ff6600,0.54:#ff0000,0.919999:#ff0000,0.92:#660000,1:#660000 --min-width 2.0 --max-width 4.0 --size 50,50 -b -v & PAUSE & EXIT 0"

ECHO Success!