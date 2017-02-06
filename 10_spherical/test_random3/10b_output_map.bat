@ECHO OFF

REM "This script generates quadrant traffic maps"

REM "Requires Python 2.7 and matplotlib (available through Anaconda)"

SET sumo_path=C:\Users\zs633\Sumo
SET output_net_path=%~dp09_output_net
SET dump_path=%~dp06_prepared
SET output_path=%~dp010b_output_map

REM "Black and white version"

START cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %output_net_path%\spherical.net.xml -i %dump_path%\modified.dump.xml,%dump_path%\modified.dump.xml -o %output_path%\spherical_bw.map.png -m quadrant,entered --default-color #808080 --default-width 0.5 --min-color-value 0 --max-color-value 130 --min-width-value 0.0 --max-width-value 100.0 --colormap #0:#000000,1:#000000 --min-width 0.5 --max-width 4.0 --size 50,50 -b -v & PAUSE & EXIT 0"

REM "Quadrant color coded version"
REM "prism for color values between 0 and 130 works well"

START /WAIT cmd.exe /K "%sumo_path%\tools\visualization\plot_net_dump.py -n %output_net_path%\spherical.net.xml -i %dump_path%\modified.dump.xml,%dump_path%\modified.dump.xml -o %output_path%\spherical_quadrant.map.png -m quadrant,entered --default-color #808080 --default-width 0.5 --min-color-value 0 --max-color-value 130 --min-width-value 0.0 --max-width-value 100.0 --colormap prism --min-width 0.5 --max-width 4.0 --size 50,50 -b -v & PAUSE & EXIT 0"

ECHO Success!