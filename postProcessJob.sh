#!/bin/bash
Ohd="4.3e-3" 
Ohf="0.1"
Ohe="8.4e-5"
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
hf="0.25"
tmax="1.0"
Ldomain="4" 
delta="0.01"
MAXlevel="9"
sigma_1="0.28"
sigma_2="0.72"


i="0" 
savefolder="/home/mark/lispread/Results/2025_09_19_Ohd_4p3e-3_Ohf_0p6_Ohe_8p4e-5_rho_d_1_rho_f_0p9_rho_e_1p2e-3_s1_0p28_s2_0p72_hf_0p25_Ldomain_4_delta_0p01_MaxLevel_10"

qcc -Wall -O2 getFacet1.c -o getFacet1 -lm -disable-dimensions
qcc -Wall -O2 getFacet2.c -o getFacet2 -lm -disable-dimensions
qcc -Wall -O2 getData.c -o getData -lm -disable-dimensions
qcc -Wall -O2 getX0Y0V0.c -o getX0Y0V0 -lm -disable-dimensions
echo "Current directory:$(pwd)"
ls -l Results/2025_09_19_Ohd_4p3e-3_Ohf_0p6_Ohe_8p4e-5_rho_d_1_rho_f_0p9_rho_e_1p2e-3_s1_0p28_s2_0p72_hf_0p25_Ldomain_4_delta_0p01_MaxLevel_10/intermediate | head
python3 Video.py $hf $Ldomain $Ohd $Ohf $Ohe $savefolder &
python3 TriplePoint.py $i $Ldomain $hf $savefolder &
wait

cd $savefolder

ffmpeg -framerate 60 -pattern_type glob -i 'TrackingTP/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p TPsim.mp4 &
ffmpeg -framerate 60 -pattern_type glob -i 'Video/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4 &
wait

cd ../