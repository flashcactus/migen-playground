set title ""
set ylabel "Использовано ПЛБ"
set xlabel "Ширина ИНС"

set autoscale

set terminal png size 800,600 enhanced font "Sans,13"
#set terminal postscript eps colour
#set output "PS.eps"

set grid
set logscale xy
set yrange [100:50000]
#set xrange [2:50]

set key right bottom

plot \
83*x**1.05 t "y=83x", 0.0035*x**5 t "y=0.0035x^5",\
"allstats4.txt" using 1:8 t "Экспериментальные данные (глубина 4)", "allstats4.txt" using 1:8 notitle smooth acsplines with lines,\
"allstats2.txt" using 1:8 t "Экспериментальные данные (глубина 2)", "allstats2.txt" using 1:8 notitle smooth acsplines with lines,\
