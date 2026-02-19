#!/bin/bash

# Base parameters (shared across runs)
rhod="1"
rhof="0.9"
rhoe="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohf_list=("5e-2")
Ohe_list=(  "9.1e-5")
tmax_list=( "20" )
Ohd_list=( 5e-3)
sigma1_list=( "0.33" )
sigma2_list=( "0.67" )
MAXlevel_list=( "12")
hf_list=("0.05")

id_start="1111"
id_end="1111"

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

SBATCH_JOB_NAME="1111b"
SBATCH_ARRAY="1111"
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/report_snapshots_overview"
PARAMS_FILE="bash_scripts/report_snapshots_overview/params_list_${SBATCH_ARRAY}.txt"
EXE="./bubbleAtLubis"
SBATCH_MEM="251G"
