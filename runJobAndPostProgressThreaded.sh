#!/bin/bash
# generated with ChatGPT
set -euo pipefail

# ---------- Base parameters (shared across runs) ----------
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
hf="0.25"
tmax="4.0"
Ldomain="4"
delta="0.01"
MAXlevel="10"
year=$(date +%Y)
month=$(date +%m)
day=$(date +%d)

# Build tag with underscores between date parts and parameters

# Compile once
qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm -disable-dimensions
qcc -Wall -O2 getFacet1.c -o getFacet1 -lm -disable-dimensions
qcc -Wall -O2 getFacet2.c -o getFacet2 -lm -disable-dimensions
qcc -Wall -O2 getData.c  -o getData  -lm -disable-dimensions
qcc -Wall -O2 getX0Y0V0.c -o getX0Y0V0 -lm -disable-dimensions

# ---------- Parameter sweeps ----------
# Edit these lists to create your combinations
Ohd_list=( "4.3e-3" )
Ohf_list=( "0.023" "0.2" "0.4" "0.6" "0.8" "1." "2." "3." "4.6" )
Ohe_list=( "8.4e-5" )
sigma1_list=( "0.28" )
sigma2_list=( "0.56" )

# Concurrency control
MAX_PAR=9           # how many sims to run at once
THREADS_PER_SIM=2   # OpenMP threads per sim (make sure MAX_PAR*THREADS_PER_SIM fits your CPU)

run_one() {
  local Ohd="$1" Ohf="$2" Ohe="$3" sigma_1="$4" sigma_2="$5"
  local tag="${year}_${month}_${day}_\
Ohd_${Ohd}_Ohf_${Ohf}_Ohe_${Ohe}_\
rho_d_${rhod}_rho_f_${rhof}_rho_e_${rhoe}_\
s1_${sigma_1}_s2_${sigma_2}_\
hf_${hf}_Ldomain_${Ldomain}_delta_${delta}_MaxLevel_${MAXlevel}"

  local folder_tag="${tag//./p}"   # Clean tag for filesystem (replace dots with d)
  local savefolder="Results/${folder_tag}"
  mkdir -p -- "$savefolder"

  (
    set -e
    export OMP_NUM_THREADS="${THREADS_PER_SIM}"

    # Run simulation
    ./bubbleAtLubis "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
                    "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder" \
                    > "${savefolder}/logTerminal" 2>&1

    # Post-process (each in its own folder)
    {
      python3 Video.py "$hf" "$Ldomain" "$Ohd" "$Ohf" "$Ohe" "$savefolder" &
      python3 TriplePoint.py "0" "$Ldomain" "$hf" "$savefolder" &
      wait
    } > "${savefolder}/logPostProcessingTerminal" 2>&1

    # Make videos (paths relative to savefolder)
    if [[ -d "$savefolder" ]]; then
      (
        cd "$savefolder"
        ffmpeg -y -framerate 60 -pattern_type glob -i 'TrackingTP/*.png' \
               -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p TPsim.mp4 \
               > ffmpeg_TP.log 2>&1 || true
        ffmpeg -y -framerate 60 -pattern_type glob -i 'Video/*.png' \
               -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4 \
               > ffmpeg_video.log 2>&1 || true
      )
    fi
  ) &
}

# Simple semaphore: cap the number of background jobs
wait_for_slot() {
  while (( $(jobs -rp | wc -l) >= MAX_PAR )); do
    wait -n
  done
}

# Launch sweep
for Ohd in "${Ohd_list[@]}"; do
  for Ohf in "${Ohf_list[@]}"; do
    for Ohe in "${Ohe_list[@]}"; do
      for sigma_1 in "${sigma1_list[@]}"; do
        for sigma_2 in "${sigma2_list[@]}"; do
          wait_for_slot
          run_one "$Ohd" "$Ohf" "$Ohe" "$sigma_1" "$sigma_2"
        done
      done
    done
  done
done

# Wait for all to finish
wait
