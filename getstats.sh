#!/bin/sh
dumpsuf="-bld.out"
statsuf="-stats.txt"
dumpfile="$@$dumpsuf"
statfile="$@$statsuf"
#build it
export PYTHONPATH="$PYTHONPATH:`pwd`:`pwd`/modules" 
python3 $@ b > "$dumpfile"

used_resrc="`grep Implemented \"$dumpfile\" | sed -E 's/^.*Implemented ([0-9]+)(( [^ ]+){2}).*$/\1\2/g'`"
used_interconnect="`grep interconnect \"$dumpfile\" | sed -E 's/^.*(average|peak).*([0-9]+%).*$/\2 \1/g'`"

echo "$used_resrc" | tee "$statfile"

echo "\ninterconnect:" | tee "$statfile"
echo "$used_interconnect" | tee "$statfile"
