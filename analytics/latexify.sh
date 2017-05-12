#!/bin/sh
sed -r -e 's/[ \t]+/ \& /g' -e 's/%/\\%/g' -e 's/$/ \\\\/'

