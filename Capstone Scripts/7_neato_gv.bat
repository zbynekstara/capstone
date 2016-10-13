@ECHO OFF

REM "Applies neato on provided gv file"

SET graphviz_path=C:\Users\Zbynda\Graphviz2\bin
SET input_path=F:\Capstone\AUH\osm\output
SET output_path=F:\Capstone\AUH\osm\output

START cmd.exe /K "%graphviz_path%\neato.exe -Tgv %input_path%\graphviz.gv -o %output_path%\graphviz.out.gv -v & PAUSE & EXIT 0"