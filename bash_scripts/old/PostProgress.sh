#!/bin/bash

# ---------- Base parameters (shared across runs) ----------
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
hf="0.05"
tmax="15"
Ldomain="5"
delta="0.01"
MAXlevel="12"

# Build tag with underscores between date parts and parameters

# Compile once
# qcc -Wall -O2 getFacet1.c -o getFacet1 -lm -disable-dimensions
# qcc -Wall -O2 getFacet2.c -o getFacet2 -lm -disable-dimensions
# qcc -Wall -O2 getData.c  -o getData  -lm -disable-dimensions
# qcc -Wall -O2 getX0Y0V0.c -o getX0Y0V0 -lm -disable-dimensions

# ---------- Parameter sweeps ----------
# Edit these lists to create your combinations
Ohd="4.6e-3" 
Ohf="20"
Ohe="8.4e-5" 
sigma1="0.28" 
sigma2="0.56" 
savefolder="Results/2025_10_05_Ohd_4p6e-3_Ohf_20,_Ohe_8p4e-5_rho_d_1_rho_f_0p9_rho_e_1p2e-3_s1_0p28_s2_0p56_hf_0p05_Ldomain_5_delta_0p01_MaxLevel_12"
  

{
python3 Video.py "$hf" "$Ldomain" "$Ohd" "$Ohf" "$Ohe" "$savefolder" &
python3 TriplePoint.py "0" "$Ldomain" "$hf" "$savefolder" &
wait
} > "${savefolder}/logPostProcessingTerminal" 2>&1
