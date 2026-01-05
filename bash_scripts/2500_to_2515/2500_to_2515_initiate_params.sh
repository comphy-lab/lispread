#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="3"
delta="0.01"

# Parameter sweeps
Ohe_list=( "5.0e-3" "2.5e-2" )
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
SBATCH_NTASKS=1         # MPI threads per sim
SBATCH_CPUS_PER_TASK=8 # OpenMP threads per sim
export OMP_NUM_THREADS="${SBATCH_CPUS_PER_TASK}"


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="2500_to_2515_start"
SBATCH_ARRAY=2500-2515
SBATCH_TIME="96:00:00"

# Node shape
SBATCH_NODES=1
SBATCH_NTASKS_PER_CORE=1

# How many of *your jobs* can fit on a 128-core node if each job uses SBATCH_NTASKS ranks
jobs_per_node=$(( 128 / SBATCH_NTASKS / SBATCH_CPUS_PER_TASK))
if (( jobs_per_node < 1 )); then
  jobs_per_node=1
fi


# Memory per job so that jobs_per_node jobs fit in 251G total on the node
# Use integer division, and clamp to at least 1G
mem_per_job_gb=$(( 251 / jobs_per_node ))
if (( mem_per_job_gb < 1 )); then
  mem_per_job_gb=1
fi
SBATCH_MEM="${mem_per_job_gb}G"

# Total CPUs requested by this job allocation (for info/logging)
TOTAL_CPUS=$(( SBATCH_NTASKS * SBATCH_CPUS_PER_TASK ))