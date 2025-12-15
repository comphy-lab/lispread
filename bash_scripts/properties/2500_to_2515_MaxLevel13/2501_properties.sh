#!/bin/bash

#############################
# Run ID  #
#############################
id_start="2500"
id_end="2515"
sub_save_folder="${id_start}_to_${id_end}_MaxLevel13/"
id_start=2501

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
Ohe_list=( "2.5e-2")
Ohf_list=( "10" )
tmax_list=( "20" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "13" )
hf_list=( "0.03" )

# Concurrency control
MAX_PAR=1         # how many sims to run at once
THREADS_PER_SIM=64 # OpenMP/MPI threads per sim


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="${id_start}_MaxLevel13"
SBATCH_TIME="96:00:00"

SBATCH_NODES=1
SBATCH_NTASKS=$(( MAX_PAR * THREADS_PER_SIM))
SBATCH_NTASKS_PER_CORE=1
SBATCH_CPUS_PER_TASK=1

