#!/bin/bash

work=$1
if [ -z $work ]; then
    work=70
fi

for i in `seq 1 10`; do
    echo "WORKING : $work"
    python Metronome.py -t $work --gradual-dura=60
    mplayer a.wav
    sleep 30
    work=$((work + 10))
done