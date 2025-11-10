#!/bin/bash

#SBATCH --partition=pm6-isw2,pm9-isw0,pm11-isw2,cn
#SBATCH --job-name=bubble_on_LIS_sweep
#SBATCH --account=ehpc-reg-2023r03-178
#SBATCH --qos=ehpc-reg-2023r03-178
#SBATCH --time=72:00:00

#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --ntasks-per-core=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=251G
#SBATCH -e job.%J.err
#SBATCH -o job.%J.out

#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.c.boulogne@student.utwente.nl

source ~/.bash_shell

set -euo pipefail

# ---------- Base parameters (shared across runs) ----------
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"
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
Ohe_list=( "5.08e-3" )
Ohf_list=( "2.5" "5" "20" "1e-2" "6e-2" "0.2" "0.5" "1" )
tmax_list=( "100" "100" "100" "5"  "100"  "100" "100" "100" )
Ohd_list=( "9.1e-5" )
sigma1_list=( "0.33" )
sigma2_list=( "0.67" )
MAXlevel_list=( "12" )
hf_list=( "0.05" )

MAX_PAR=8           # how many sims to run at once
THREADS_PER_SIM=16   # OpenMP threads per sim (make sure MAX_PAR*THREADS_PER_SIM fits available cores)

run_one() {
  local Ohd="$1" Ohf="$2" Ohe="$3" sigma_1="$4" sigma_2="$5" MAXlevel="$6" hf="$7" tmax="$8"
  local tag="${year}_${month}_${day}_\
Ohd_${Ohd}_Ohf_${Ohf}_Ohe_${Ohe}_\
rho_d_${rhod}_rho_f_${rhof}_rho_e_${rhoe}_\
s1_${sigma_1}_s2_${sigma_2}_\
hf_${hf}_Ldomain_${Ldomain}_delta_${delta}_MaxLevel_${MAXlevel}"

  local folder_tag="${tag//./p}"   # Clean tag for filesystem (replace dots with d)
  local savefolder="Results/bubble/${folder_tag}"
  mkdir -p -- "$savefolder"

  (
    set -e
    export OMP_NUM_THREADS="${THREADS_PER_SIM}"

    # Calculate_tmax

    # Run simulation
    ./bubbleAtLubis "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
                    "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder" \
                    > "${savefolder}/logTerminal" 2>&1
  ) &
}

# Cap the number of background jobs
wait_for_slot() {
  while (( $(jobs -rp | wc -l) >= MAX_PAR )); do
    wait -n
  done
}

# Launch sweep
for MAXlevel in "${MAXlevel_list[@]}"; do
  for Ohd in "${Ohd_list[@]}"; do
    for hf in "${hf_list[@]}"; do
      for i in "${!Ohf_list[@]}"; do
        Ohf="${Ohf_list[$i]}"
        tmax="${tmax_list[$i]}"
        for Ohe in "${Ohe_list[@]}"; do
          for sigma_1 in "${sigma1_list[@]}"; do
            for sigma_2 in "${sigma2_list[@]}"; do
              wait_for_slot
              run_one "$Ohd" "$Ohf" "$Ohe" "$sigma_1" "$sigma_2" "$MAXlevel" "$hf" "$tmax"
            done
          done
        done
      done
    done
  done
done

# Wait for all to finish
wait
