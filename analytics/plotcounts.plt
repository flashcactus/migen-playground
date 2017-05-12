set title ""
set ylabel "Использовано DSP-блоков"
set xlabel "Ширина ИНС"

set autoscale

set terminal png size 1600,900 enhanced font "Sans,13"
#set terminal postscript eps colour
#set output "PS.eps"

set grid

plot "stats.txt" using 1:7 notitle, \
    "stats1.txt" using 1:7 t "d=1" smooth acsplines with lines,\
    "stats2.txt" using 1:7 t "d=2" smooth acsplines with lines,\
    "stats3.txt" using 1:7 t "d=3" smooth acsplines with lines,\
    "stats4.txt" using 1:7 t "d=4" smooth acsplines with lines
