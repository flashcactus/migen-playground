#!/bin/sh
for f in bdata/*stats.txt; do
    params="`echo $f | sed -E 's/^[^ ]* (.*)-stats.txt$/\1/'`"
    cells="`grep -m 1 cells \"$f\" | awk '{print $1}'`"
    dsp="`grep -m 1 DSP \"$f\" | awk '{print $1}'`"
    ic_avg="`grep -m 1 '% average' \"$f\"  | awk '{print $1}'`"
    ic_peak="`grep -m 1 '% peak' \"$f\"  | awk '{print $1}'`"
    neuredg="`grep -m 1 'Rectnet' \"$f\"  | sed -E 's/^.* ([0-9]+) neurons.* ([0-9]+) edges.*$/\1 \2/g'`"
    if [ -z "$cells" ]; then
        echo "cells empty; killing file $f" 1>&2
        rm "$f"
        continue
    fi
    if [ -z "$neuredg" ]; then
        neuredg="- -"
    fi
    echo "$params\t$neuredg\t$cells\t$dsp\t$ic_avg\t$ic_peak"
done

