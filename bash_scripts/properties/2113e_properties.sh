#!/bin/bash

#############################
# Run ID  #
#############################
id_start="2113e"
id_end="2113e"
sub_save_folder="${id_start}/"


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
Ohe_list=( "1.0e-3" )
Ohf_list=( "5")
tmax_list=( "10" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "12" )
hf_list=( "0.05" )

# Concurrency control
MAX_PAR=1         # how many sims to run at once
THREADS_PER_SIM=32 # OpenMP/MPI threads per sim


#############################
# SBATCH related parameters #
#############################

SBATCH_JOB_NAME="${id_start}"
SBATCH_TIME="96:00:00"

SBATCH_NODES=1
SBATCH_NTASKS=$((MAX_PAR * THREADS_PER_SIM))
SBATCH_NTASKS_PER_CORE=1
SBATCH_CPUS_PER_TASK=1

