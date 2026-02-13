#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
R=$(awk 'BEGIN { printf "%.10f", 150/650 }')

# sqrt(1/R)
sqrt_inv_R=$(awk -v R="$R" 'BEGIN { printf "%.10f", sqrt(1/R) }')

#############################
# Parameter sweeps
#############################

# Ohd = 5e-3 * sqrt(1/R)
Ohe_list=(
  "$(awk -v s="$sqrt_inv_R" 'BEGIN { printf "%.10f", 5e-3 * s }')"
)

# Ohe = 9.1e-5 * sqrt(1/R)
Ohd_list=(
  "$(awk -v s="$sqrt_inv_R" 'BEGIN { printf "%.10f", 9.1e-5 * s }')"
)

# Ohf values
Ohf_base=( 7.5 10 15 20 30 50 100 200)
Ohf_list=()

for v in "${Ohf_base[@]}"; do
  Ohf_list+=(
    "$(awk -v v="$v" -v s="$sqrt_inv_R" 'BEGIN { printf "%.10f", v * s }')"
  )
done

# tmax values
tmax_base=( 10 10 10 10 10 10 10 10 )
tmax_list=()

for v in "${tmax_base[@]}"; do
  tmax_list+=(
    "$(awk -v v="$v" -v s="$sqrt_inv_R" 'BEGIN { printf "%.10f", v * s }')"
  )
done

sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "12")
hf_list=( "$(echo "0.05 / $R" | bc -l)" )

id_start="3342"
id_end="3349"

sims_simultaneously=$((id_end - id_start + 1))

# Concurrency control
SBATCH_CPUS_PER_TASK=32 # OpenMP threads per sim
SBATCH_NTASKS=1 # MPI threads per sim
export OMP_NUM_THREADS=32

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="3342_to_3349"
SBATCH_ARRAY="3342-3349"
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"
PARAMS_FILE="bash_scripts/3210_to_3242/params_list_${SBATCH_ARRAY}_start.txt"
EXE="./bubbleAtLubis"
SBATCH_MEM="251G"
