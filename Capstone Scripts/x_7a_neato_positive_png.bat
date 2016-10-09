@ECHO OFF

REM "Applies neato on provided gv file"

SET graphviz_path=C:\Users\Zbynda\Graphviz2\bin
SET input_path=F:\Capstone\AUH\osm\output
SET output_path=F:\Capstone\AUH\osm\output

START cmd.exe /K "%graphviz_path%\neato.exe -Tpng -Gsize=20,20 -Gdpi=100 %input_path%\graphviz.pos.out.gv -o %output_path%\graphviz.pos.out.png -v & PAUSE & EXIT 0"