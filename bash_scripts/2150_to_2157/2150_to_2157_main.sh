#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohe_list=( "1e-3" "5e-3" )
Ohf_list=( "1" "2.5" "5" "10" )
tmax_list=( "10" "10" "10" "10" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "12" )
hf_list=("0.05" )

id_start="2150"
id_end="2157"


# Concurrency control
SBATCH_CPUS_PER_TASK=1 # OpenMP threads per sim
SBATCH_NTASKS=16 # MPI threads per sim
export OMP_NUM_THREADS=1

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="2150_to_2157"
SBATCH_ARRAY=2150-2157
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"
PARAMS_FILE="bash_scripts/2150_to_2157/params_list_${SBATCH_ARRAY}.txt"
EXE="./bubbleAtLubis_unaltered_3phase_mpi"
SBATCH_MEM="64G"
