#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohf_list=("1e-2")
Ohe_list=(  "9.1e-5")
tmax_list=( "1" )
Ohd_list=( 5e-3)
sigma1_list=( "0.33" )
sigma2_list=( "0.67" )
MAXlevel_list=( "9")
hf_list=("0.1")

id_start="4000"
id_end="4000"

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

SBATCH_JOB_NAME="4000"
SBATCH_ARRAY="4000-4000"
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"
PARAMS_FILE="bash_scripts/4000/params_list_${SBATCH_ARRAY}.txt"
EXE="./bubbleAtLubis_unfiltered"
SBATCH_MEM="251G"
