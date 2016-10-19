@ECHO OFF

REM "Applies neato on provided gv file"
REM "Change Gepsilon value to determine granularity/speed tradeoff of solver (default 0.0001)"
REM "Change Gmaxiter value to force cutoff of solver (default 200)"

SET graphviz_path=C:\Users\zs633\Graphviz2\bin
SET input_path=C:\Users\zs633\Capstone\AUH\osm\output
SET output_path=C:\Users\zs633\Capstone\AUH\osm\output

START cmd.exe /K "%graphviz_path%\neato.exe -Gepsilon=0.0001 -Gmaxiter=200 -Tgv %input_path%\graphviz.gv -o %output_path%\graphviz.out.gv -v & PAUSE & EXIT 0"