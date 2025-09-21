#!/bin/bash



Ohd="4.3e-3" 
Ohf="4.6"
Ohe="8.4e-5"
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
hf="0.25"
tmax="0.5"
Ldomain="4" 
delta="0.01"
MAXlevel="9"
sigma_1="0.28"
sigma_2="0.72"
i="0" 
savefolder="Results/verify_Ohf4p6" 

qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm -disable-dimensions
qcc -Wall -O2 getFacet1.c -o getFacet1 -lm -disable-dimensions
qcc -Wall -O2 getFacet2.c -o getFacet2 -lm -disable-dimensions
qcc -Wall -O2 getData.c -o getData -lm -disable-dimensions
qcc -Wall -O2 getX0Y0V0.c -o getX0Y0V0 -lm -disable-dimensions
export OMP_NUM_THREADS=4
# rm dump
# rm -r intermediate/*

# From here below I want to run multiple simulations with different parameters simultaneously
./bubbleAtLubis $Ohd $Ohf $Ohe $rhod $rhof $rhoe $sigma_1 $sigma_2 $hf $tmax $Ldomain $delta $MAXlevel $savefolder
{
    echo "Current directory:$(pwd)"
    python3 Video.py $hf $Ldomain $Ohd $Ohf $Ohe $savefolder &
    python3 TriplePoint.py $i $Ldomain $hf $savefolder &
    wait

} > $savefolder/logPostProcess 2>&1

cd $savefolder

ffmpeg -framerate 60 -pattern_type glob -i 'TrackingTP/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p TPsim.mp4 &
ffmpeg -framerate 60 -pattern_type glob -i 'Video/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4 &
wait

cd ../