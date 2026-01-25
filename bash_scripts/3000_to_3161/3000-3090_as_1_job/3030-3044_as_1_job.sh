#!/bin/bash


id_start="3030"
id_end="3044"

sims_simultaneously=$((id_end - id_start + 1))

# Concurrency control
SBATCH_CPUS_PER_TASK=252 # OpenMP threads per sim
SBATCH_NTASKS=1 # MPI threads per sim
export OMP_NUM_THREADS=16
omp_num_threads=16

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="3000_to_3089"
SBATCH_ARRAY="3000-3089"
SBATCH_TIME="96:00:00"

# base save directory
base_save_dir="Results/${SBATCH_ARRAY}"
PARAMS_FILE="bash_scripts/3000_to_3161/params_list_${SBATCH_ARRAY}.txt"
EXE="./bubbleAtLubis_unaltered_3phase"
SBATCH_MEM="251G"
