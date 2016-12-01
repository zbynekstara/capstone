@ECHO OFF

REM "Applies neato on provided gv file"
REM "Change Gepsilon value to determine granularity/speed tradeoff of solver (default 0.0001)"
REM "Change Gmaxiter value to force cutoff of solver (default 200)"

SET graphviz_path=C:\Users\zs633\Graphviz2\bin
SET prepared_path=%~dp06_prepared
SET displaced_path=%~dp07_displaced

START /WAIT cmd.exe /K "%graphviz_path%\neato.exe -Gepsilon=0.01 -Gmaxiter=200 -Tgv %prepared_path%\graphviz.gv -o %displaced_path%\graphviz.out.gv -v & PAUSE & EXIT 0"

ECHO Success!