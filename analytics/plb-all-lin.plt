set title ""
set ylabel "Использовано ПЛБ"
set xlabel "Ширина ИНС"

set autoscale

set terminal png size 800,600 enhanced font "Sans,13"
#set terminal postscript eps colour
#set output "PS.eps"

set grid
#set logscale y

plot "allstats1.txt" using 1:8 notitle, "allstats1.txt" using 1:8 notitle smooth acsplines with lines,\
     "allstats2.txt" using 1:8 notitle, "allstats2.txt" using 1:8 notitle smooth acsplines with lines,\
     "allstats3.txt" using 1:8 notitle, "allstats3.txt" using 1:8 notitle smooth acsplines with lines,\
     "allstats4.txt" using 1:8 notitle, "allstats4.txt" using 1:8 notitle smooth acsplines with lines,\
     "allstats5.txt" using 1:8 notitle, "allstats5.txt" using 1:8 notitle smooth acsplines with lines,\
     "allstats10.txt" using 1:8 notitle, "allstats10.txt" using 1:8 notitle smooth acsplines with lines,
