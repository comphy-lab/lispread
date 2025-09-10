#!/bin/bash


Oho="1e-2" 
Ohw="1e-2"
Oha="5e-5"
hf="0.25"
tmax="1.0"
Ldomain="4"
delta="0.01"
MAXlevel="11"
i="0" 
{
    qcc -Wall -O2 getFacet1.c -o getFacet1 -lm -disable-dimensions
    qcc -Wall -O2 getFacet2.c -o getFacet2 -lm -disable-dimensions
    qcc -Wall -O2 getData.c -o getData -lm -disable-dimensions
    echo "Current directory:$(pwd)"
    python3 Video.py $hf $Ldomain $Oho $Ohw &
    python3 TriplePoint.py $i $Ldomain $hf &
    wait




} > logPostProcess 2>&1


ffmpeg -framerate 60 -pattern_type glob -i 'TrackingTP/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p $i-TP2.mp4 &
ffmpeg -framerate 60 -pattern_type glob -i 'Video/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p test2-python.mp4 &
wait
