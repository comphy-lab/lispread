#!/bin/bash



Oho="1e-2" 
Ohw="1e-2"
Oha="5e-5"
hf="0.25"
tmax="2.0"
Ldomain="4" 
delta="0.01"
MAXlevel="9"


qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm -disable-dimensions
export OMP_NUM_THREADS=4
rm dump
rm -r intermediate/*
./bubbleAtLubis $Oho $Ohw $Oha $hf $tmax $Ldomain $delta $MAXlevel
