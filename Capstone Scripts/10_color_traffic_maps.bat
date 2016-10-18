@ECHO OFF

REM "This script generates traffic color maps"
REM "Requires Python 2.7"
REM "Requires matplotlib (available through Anaconda)"

SET sumo_path="C:\Users\zs633\Sumo"
SET osm_path=C:\Users\zs633\Capstone\AUH\osm
SET data_path=%osm_path%\output

START cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %osm_path%\island.net.xml -i %data_path%\modified.dump.xml,%data_path%\modified.dump.xml -o %data_path%\island_colormap.rdylgn.png -m diff_speed_ratio,occupancy --default-color #808080 --default-width 2 --min-color-value 0.0 --max-color-value 1.0 --min-width-value 0.0 --max-width-value 100.0 --colormap RdYlGn_r --min-width 2 --max-width 2 --size 50,50 --xlim 2000,22000 --ylim -5000,21000 -b -v & PAUSE & EXIT 0"

START cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %osm_path%\island.net.xml -i %data_path%\modified.dump.xml,%data_path%\modified.dump.xml -o %data_path%\island_colormap.google.png -m diff_speed_ratio,occupancy --default-color #808080 --default-width 2 --min-color-value 0.0 --max-color-value 1.0 --min-width-value 0.0 --max-width-value 100.0 --colormap #0.0:#00cc00,0.499999:#00cc00,0.5:#ff6600,0.749999:#ff6600,0.75:#ff0000,0.949999:#ff0000,0.95:#660000,1.0:#660000 --min-width 2 --max-width 2 --size 50,50 --xlim 2000,22000 --ylim -5000,21000 -b -v & PAUSE & EXIT 0"