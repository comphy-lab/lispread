#!/bin/bash

#############################
# Run ID  #
#############################
id_start="2500"
id_end="2507"
sub_save_folder="${id_start}_to_${id_end}/"


###################################
# Simulation and sweep parameters #
###################################

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="3"
delta="0.01"

# Parameter sweeps
Ohe_list=( "5.0e-3" "2.5e-2")
Ohf_list=( "10" "20" "30" "40")
tmax_list=( "1" "1.5" "2" "2.5" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "10" )
hf_list=( "0.03" )

# Concurrency control
MAX_PAR=8         # how many sims to run at once
THREADS_PER_SIM=8 # OpenMP/MPI threads per sim


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="${id_start}_to_${id_end}"
SBATCH_TIME="96:00:00"

SBATCH_NODES=1
SBATCH_NTASKS=$(( MAX_PAR * THREADS_PER_SIM / 2 ))
SBATCH_NTASKS_PER_CORE=1
SBATCH_CPUS_PER_TASK=2

