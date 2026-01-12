#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="3"
delta="0.01"

# Parameter sweeps
Ohe_list=( "1e-3" "5e-3" )
Ohf_list=( "10" "20" "30" "40" )
tmax_list=( "0.01" "0.01" "0.01" "0.01" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "11" )
hf_list=( "0.03" "0.05" )

id_start="2500"
id_end="2515"

PARAMS_FILE="bash_scripts/2500_to_2515/params_list_${id_start}_to_${id_end}_initiate.txt"
EXE="./bubbleAtLubis"

# Concurrency control
MPI_RANKS=1         # MPI threads per sim
SBATCH_CPUS_PER_TASK=8 # OpenMP threads per sim
SBATCH_NTASKS=1 
export OMP_NUM_THREADS="${SBATCH_CPUS_PER_TASK}"


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="2500_to_2515_init"
SBATCH_ARRAY=2500-2515
SBATCH_TIME="96:00:00"

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=2

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"