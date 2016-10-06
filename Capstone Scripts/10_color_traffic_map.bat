@ECHO OFF

REM "This script generates a color map of traffic"
REM "Requires Python 2.7"
REM "Requires matplotlib (available through Anaconda)"

SET sumo_path="C:\Users\Zbynda\Sumo"
SET osm_path=F:\Capstone\AUH\osm
SET data_path=%osm_path%\duarouter

START cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %osm_path%\island.net.xml -i %data_path%\island.dump.xml,%data_path%\island.dump.xml -o %data_path%\island.map.png -m occupancy,occupancy --default-color #808080 --default-width 2 --min-color-value 0.0 --max-color-value 100.0 --min-width-value 0.0 --max-width-value 100.0 --colormap RdYlGn_r --min-width 2 --max-width 2 --size 50,50 --xlim 2000,22000 --ylim -5000,21000 -b -v & PAUSE & EXIT 0"