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
tmax_list=( "0.2" "0.25" "0.5" "0.5" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "11" )
hf_list=( "0.03" "0.05" )

id_start="2500"
id_end="2515"
PARAMS_FILE="bash_scripts/2500_to_2515/params_list_${id_start}_to_${id_end}_start.txt"


# Concurrency control
SBATCH_NTASKS=16         # how many sims to run at once
SBATCH_CPUS_PER_TASK=16 # OpenMP/MPI threads per sim


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="2500_to_2515_start"
SBATCH_ARRAY=2500-2515
SBATCH_TIME="96:00:00"

TOTAL_CPUS=$((SBATCH_NTASKS * SBATCH_CPUS_PER_TASK))
SBATCH_NODES=$(( (TOTAL_CPUS + 127) / 128 ))
SBATCH_NTASKS_PER_CORE=1

