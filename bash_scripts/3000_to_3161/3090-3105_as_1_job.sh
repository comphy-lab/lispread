#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohd_list=( "5e-3" )
Ohf_list=( "0.01" "0.05" "0.1" "0.5" "1" "2.5" "5" "7.5" "10")
tmax_list=( "3" "3" "3" "4" "5" "10" "10" "12" "12")
Ohe_list=( "5e-5" "8e-5" "1.2e-3" "1.5e-5")
sigma1_list=( "0.33" )
sigma2_list=( "0.67" )
MAXlevel_list=("11")
hf_list=("0.05")

id_start="3090"
id_end="3105"

sims_simultaneously=$((id_end - id_start + 1))

# Concurrency control
SBATCH_CPUS_PER_TASK=252 # OpenMP threads per sim
SBATCH_NTASKS=1 # MPI threads per sim
export OMP_NUM_THREADS=15
omp_num_threads=15

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="3090_to_3125"
SBATCH_ARRAY="3090-3125"
SBATCH_TIME="48:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"
PARAMS_FILE="bash_scripts/3000_to_3161/params_list_${SBATCH_ARRAY}.txt"
EXE="./bubbleAtLubis_unaltered_3phase"
SBATCH_MEM="251G"
