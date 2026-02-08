#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
R=$(echo "scale=10; 2000/650" | bc -l)
sqrt_inv_R=$(echo "scale=10; sqrt(1/$R)" | bc -l)
Ohd_list=( "$(echo "5e-3 * $sqrt_inv_R" | bc -l)" )
Ohe_list=( "$(echo "9.1e-5 * $sqrt_inv_R" | bc -l)" )

Ohf_base=( "0.001" "0.005" "0.01" "0.05" "0.1" "1" "2.5" "5")
Ohf_list=()
for v in "${Ohf_base[@]}"; do
  Ohf_list+=( "$(echo "$v * $sqrt_inv_R" | bc -l)" )
done

tmax_base=( "3" "3" "3" "3" "3" "4" "5" "6")
tmax_list=()
for v in "${tmax_base[@]}"; do
  tmax_list+=( "$(echo "$v * $sqrt_inv_R" | bc -l)" )
done

sigma1_list=( "0.33" )
sigma2_list=( "0.67" )
MAXlevel_list=( "12")
hf_list=( "$(echo "0.05 / $R" | bc -l)" )

id_start="3226"
id_end="3233"

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

SBATCH_JOB_NAME="3226_to_3233"
SBATCH_ARRAY="3226-3233"
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"
PARAMS_FILE="bash_scripts/3210_to_3242/params_list_${SBATCH_ARRAY}_start.txt"
EXE="./bubbleAtLubis"
SBATCH_MEM="251G"
