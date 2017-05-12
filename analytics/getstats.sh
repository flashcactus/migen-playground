#!/bin/sh
dumpsuf="-bld.out"
statsuf="-stats.txt"
dumpfile="bdata/$@$dumpsuf"
statfile="bdata/$@$statsuf"
#build it
export PYTHONPATH="$PYTHONPATH:`pwd`/..:`pwd`/../modules" 
if [ -e "$dumpfile" ] && grep "!!OK!!" "$dumpfile"; then
    echo "Already built"
else
    python3 $@ b > "$dumpfile" 2>&1 && echo "!!OK!!" >>"$dumpfile"
fi

used_resrc="`grep Implemented \"$dumpfile\" | sed -E 's/^.*Implemented ([0-9]+)(( [^ ]+){2}).*$/\1\2/g'`"
used_interconnect="`grep interconnect \"$dumpfile\" | sed -E 's/^.*(average|peak).*([0-9]+%).*$/\2 \1/g'`"


date >> "$statfile"
grep Rectnet "$dumpfile" | tee -a "$statfile"
echo "$used_resrc" | tee -a "$statfile"
echo "$used_interconnect" | tee -a "$statfile"
