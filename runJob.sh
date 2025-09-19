#!/bin/bash



Ohd="4.3e-3" 
Ohf="0.1"
Ohe="8.4e-5"
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
hf="0.25"
tmax="2.0"
Ldomain="4" 
delta="0.01"
MAXlevel="9"
sigma_1="0.28"
sigma_2="0.72"

qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm -disable-dimensions
export OMP_NUM_THREADS=4
# rm dump
# rm -r intermediate/*
./bubbleAtLubis $Ohd $Ohf $Ohe $rhod $rhof $rhoe $sigma_1 $sigma_2 $hf $tmax $Ldomain $delta $MAXlevel
