#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohf_list=("5e-2")
Ohd_list=(  "9.1e-5")
tmax_list=( "20" )
Ohe_list=( 5e-3)
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "12")
hf_list=("0.05")

id_start="2111"
id_end="2111"

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

SBATCH_JOB_NAME="2111b"
SBATCH_ARRAY="2111"
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/report_snapshots_overview"
PARAMS_FILE="bash_scripts/report_snapshots_overview/params_list_${SBATCH_ARRAY}.txt"
EXE="./bubbleAtLubis"
SBATCH_MEM="251G"
