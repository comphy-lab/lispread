#!/bin/bash

#SBATCH --partition=pm6-isw2,pm9-isw0,pm11-isw2,cn
#SBATCH --job-name=2001_to_2016
#SBATCH --account=ehpc-reg-2023r03-178
#SBATCH --qos=ehpc-reg-2023r03-178
#SBATCH --time=96:00:00

#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --tasks-per-node=24
#SBATCH --cpus-per-task=8
#SBATCH --mem=251G
#SBATCH -e job.%J.err
#SBATCH -o job.%J.out

#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.c.boulogne@student.utwente.nl
#SBATCH --array=2500-2515

set -euo pipefail

source ~/.bash_shell

# --- paths / constants ---
PARAMS_FILE="bash_scripts/mpi_params/params_2500_to_2515_start.txt"
EXE="./bubbleAtLubis_mpi"

Ldomain="5"
# If delta and MAXlevel are in the params file already, these constants are not used.
# Keep Ldomain here since your params generator didn't include it.

# Where to store outputs (change as you like)
BASE_SAVE_DIR="$PWD/Results"

# --- select the line for this array task ---
task_id="${SLURM_ARRAY_TASK_ID}"

# Find the line whose first column equals the task id
line="$(awk -v id="$task_id" '$1==id {print; exit}' "$PARAMS_FILE")"

if [[ -z "${line}" ]]; then
  echo "ERROR: No line found for runid=$task_id in $PARAMS_FILE" >&2
  exit 1
fi

# Parse columns from the line
# Format: runid Ohd Ohf Ohe rhod rhof rhoe sigma_1 sigma_2 hf MAXlevel delta tmax
read -r runid Ohd Ohf Ohe rhod rhof rhoe sigma_1 sigma_2 hf Ldomain MAXlevel delta tmax <<< "$line"

savefolder="${BASE_SAVE_DIR}/test_${runid}"
mkdir -p "$savefolder"

echo "RunID: $runid"
echo "Params: Ohd=$Ohd Ohf=$Ohf Ohe=$Ohe rhod=$rhod rhof=$rhof rhoe=$rhoe sigma_1=$sigma_1 sigma_2=$sigma_2 hf=$hf tmax=$tmax Ldomain=$Ldomain delta=$delta MAXlevel=$MAXlevel"
echo "Savefolder: $savefolder"
echo "SLURM job: ${SLURM_JOB_ID:-NA} task: ${SLURM_ARRAY_TASK_ID:-NA}"

# save parameters to a log file
params_log="${savefolder}/parameters.txt"

{
  echo "=== Simulation start ==="
  echo "start_time = $(date -Is)"
  echo "runid = $runid"
  echo "job_id = ${SLURM_JOB_ID:-NA}"
  echo "array_task_id = ${SLURM_ARRAY_TASK_ID:-NA}"
  echo "host = $(hostname)"

  echo "Ohd = $Ohd"
  echo "Ohf = $Ohf"
  echo "Ohe = $Ohe"
  echo "rhod = $rhod"
  echo "rhof = $rhof"
  echo "rhoe = $rhoe"
  echo "sigma_1 = $sigma_1"
  echo "sigma_2 = $sigma_2"
  echo "hf = $hf"
  echo "tmax = $tmax"
  echo "Ldomain = $Ldomain"
  echo "delta = $delta"
  echo "MAXlevel = $MAXlevel"
  echo "========================"
  echo
} >> "$params_log"


# --- run ---
# Use -n to match how many MPI ranks you want.
# Here I use all allocated tasks (24). Change if your code expects a different count.
# srun -n "${SLURM_NTASKS}" "$EXE" \
#   "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
#   "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder"
