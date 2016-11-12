@ECHO OFF

REM "This script generates traffic color maps"
REM "Requires Python 2.7 and matplotlib (available through Anaconda)"
REM "This can be run after step 6"

REM "Google colormap: 65-50/65 = green, 50-30/65 = orange, 30-5/65 = red, 5-0/65 = dark red"
REM "In terms of slowdown_ratio: 0.00-0.23, 0.23-0.54, 0.54-0.92, 0.92-1.00"

SET sumo_path=C:\Users\zs633\Sumo
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET net_path=%osm_path%\output_net
SET data_path=%osm_path%\output
SET output_path=%osm_path%\info

START /WAIT cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %net_path%\lensing.net.xml -i %data_path%\modified.dump.xml,%data_path%\modified.dump.xml -o %output_path%\lensing.map.png -m slowdown_ratio,entered --default-color #808080 --default-width 0.5 --min-color-value 0.0 --max-color-value 1.0 --min-width-value 0.0 --max-width-value 100.0 --colormap #0:#000000,1:#000000 --min-width 0.5 --max-width 4.0 --size 50,50 -b -v & PAUSE & EXIT 0"

ECHO Success!