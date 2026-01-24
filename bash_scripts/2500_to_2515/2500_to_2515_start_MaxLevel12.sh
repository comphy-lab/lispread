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
tmax_list=( "20" "20" "20" "20" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "12" )
hf_list=( "0.03" "0.05" )

id_start="2500"
id_end="2515"


sims_simultaneously=$((id_end - id_start + 1))
# Concurrency control
SBATCH_CPUS_PER_TASK=1 # OpenMP threads per sim
SBATCH_NTASKS=16 # Total MPI threads per sweep
mpi_ranks=16
export OMP_NUM_THREADS=1

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="2500_to_2515_MaxLevel12"
SBATCH_ARRAY=2500-2515
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}_MaxLevel_12"
PARAMS_FILE="bash_scripts/2500_to_2515/params_list_${SBATCH_ARRAY}_MaxLevel12.txt"
EXE="./bubbleAtLubis_mpi"
SBATCH_MEM="251G"
