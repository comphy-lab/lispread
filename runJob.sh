#!/bin/bash



Oho="1e-2" 
Ohw="1e-2"
Oha="5e-5"
hf="0.25"
tmax="1.0"
Ldomain="3.5"
delta="0.01"
MAXlevel="8"


qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm -disable-dimensions
export OMP_NUM_THREADS=4
./bubbleAtLubis $Oho $Ohw $Oha $hf $tmax $Ldomain $delta $MAXlevel
