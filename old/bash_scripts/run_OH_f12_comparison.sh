#!/usr/bin/env bash
# run_sims.sh — fixed & screen-friendly
set -Eeuo pipefail

# ---------- Base parameters (shared across runs) ----------
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
hf="0.031"
tmax_normal="3.0"
Ldomain="5"
delta="0.01"
MAXlevel="10"
year=$(date +%Y)
month=$(date +%m)
day=$(date +%d)

Ohd="4.6e-3"
Ohf="0.44"
Ohe="8.4e-5"
sigma_1="0.28"
sigma_2="0.56"

# Concurrency control
MAX_PAR=4           # not used below, keep for future sweeps
THREADS_PER_SIM=5   # OpenMP threads per sim

# Build tag
tag="${year}_${month}_${day}_\
Ohd_${Ohd}_Ohf_${Ohf}_Ohe_${Ohe}_\
rho_d_${rhod}_rho_f_${rhof}_rho_e_${rhoe}_\
s1_${sigma_1}_s2_${sigma_2}_\
hf_${hf}_Ldomain_${Ldomain}_delta_${delta}_MaxLevel_${MAXlevel}"

# Filesystem-safe tag (replace '.' with 'p')
folder_tag="${tag//./p}"

# ---------- Env ----------
export OMP_NUM_THREADS="${THREADS_PER_SIM}"

# ---------- Requirements check ----------
need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 127; }; }
need bc
need ffmpeg
need python3
# Binaries (adjust names/paths as needed)
[[ -x ./bubbleAtLubisU ]] || { echo "Missing executable: ./bubbleAtLubisU" >&2; exit 127; }
# Optional tools, only used if you uncomment those calls:
# need qcc

# ---------- Helpers ----------
calc_tmax() {
  # tmax = tmax_normal * sqrt(Ohf / 0.023)
  echo "$(echo "$tmax_normal * sqrt($Ohf / 0.023)" | bc -l)"
}

make_videos() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0
  (
    cd "$dir"
    ffmpeg -y -framerate 60 -pattern_type glob -i 'TrackingTP/*.png' \
      -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p TPsim.mp4 \
      > ffmpeg_TP.log 2>&1 || true
    ffmpeg -y -framerate 60 -pattern_type glob -i 'Video/*.png' \
      -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4 \
      > ffmpeg_video.log 2>&1 || true
  )
}

# ---------- tmax ----------
tmax="$(calc_tmax)"
echo "Computed tmax = $tmax"

# ==========================================================
# ===============   RUN 1: “new_Oh” (disabled)   ===========
# ==========================================================
# Uncomment this block if/when you want to run the “new_Oh” variant.

savefolder_new="Results/${folder_tag}_new_Oh"
# mkdir -p -- "$savefolder_new"
# echo "Running NEW Oh case -> $savefolder_new"
# # Example compile (once)
# # qcc -fopenmp -Wall -O2 bubbleAtLubis.c -o bubbleAtLubis -lm -disable-dimensions
# # qcc -Wall -O2 getFacet1.c -o getFacet1 -lm -disable-dimensions
# # qcc -Wall -O2 getFacet2.c -o getFacet2 -lm -disable-dimensions
# # qcc -Wall -O2 getData.c  -o getData  -lm -disable-dimensions
# # qcc -Wall -O2 getX0Y0V0.c -o getX0Y0V0 -lm -disable-dimensions
#
# ./bubbleAtLubis "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
#   "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder_new" \
#   > "${savefolder_new}/logTerminal" 2>&1
#
# {
#   python3 Video.py "$hf" "$Ldomain" "$Ohd" "$Ohf" "$Ohe" "$savefolder_new" &
#   python3 TriplePoint.py "0" "$Ldomain" "$hf" "$savefolder_new" &
#   wait
# } > "${savefolder_new}/logPostProcessingTerminal" 2>&1
#
make_videos "$savefolder_new"

# ==========================================================
# ===============   RUN 2: “old_Oh” (active)    ===========
# ==========================================================
savefolder_old="Results/${folder_tag}_old_Oh"
mkdir -p -- "$savefolder_old"
echo "Running OLD Oh case -> $savefolder_old"

./bubbleAtLubisU "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
  "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder_old" \
  > "${savefolder_old}/logTerminal" 2>&1

{
  python3 Video.py "$hf" "$Ldomain" "$Ohd" "$Ohf" "$Ohe" "$savefolder_old" &
  python3 TriplePoint.py "0" "$Ldomain" "$hf" "$savefolder_old" &
  wait
} > "${savefolder_old}/logPostProcessingTerminal" 2>&1

make_videos "$savefolder_old"

echo "All done."
