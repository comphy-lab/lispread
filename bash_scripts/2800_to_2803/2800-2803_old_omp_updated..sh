#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohe_list=( "5e-3" )
Ohf_list=( "0.5" "5" )
tmax_list=( "10" "10" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "11" )
hf_list=("0.05" "0.03")

id_start="2800"
id_end="2803"

sims_simultaneously=$((id_end - id_start + 1))

# Concurrency control
SBATCH_CPUS_PER_TASK=16 # OpenMP threads per sim
SBATCH_NTASKS=1 # MPI threads per sim
export OMP_NUM_THREADS=16

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="2800_to_2803"
SBATCH_ARRAY=2800-2803
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}_old_omp_updated"
PARAMS_FILE="bash_scripts/2800_to_2803/params_list_${SBATCH_ARRAY}_old_omp_updated.txt"
EXE="./bubbleAtLubis_unaltered_3phase"
SBATCH_MEM="251G"
