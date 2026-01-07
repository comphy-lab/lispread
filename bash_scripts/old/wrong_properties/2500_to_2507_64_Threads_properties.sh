#!/bin/bash

#############################
# Run ID  #
#############################
id_start="2502"
id_end="2503"
sub_save_folder="2500_to_2507_64Threads/"


###################################
# Simulation and sweep parameters #
###################################

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohe_list=( "5.0e-3" "2.5e-2")
Ohf_list=("20")
tmax_list=( "20")
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "13" )
hf_list=( "0.05" )

# Concurrency control
MAX_PAR=2         # how many sims to run at once
THREADS_PER_SIM=64 # OpenMP/MPI threads per sim


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="${id_start}_to_${id_end}_64Threads"
SBATCH_TIME="1:00:00"

SBATCH_NODES=1
SBATCH_NTASKS=$(( MAX_PAR * THREADS_PER_SIM))
SBATCH_NTASKS_PER_CORE=1
SBATCH_CPUS_PER_TASK=1

