#!/bin/bash

#############################
# standard SBATCH parameters #
#############################

SBATCH_PARTITION="pm6-isw2,pm9-isw0,pm11-isw2,cn"
SBATCH_ACCOUNT="ehpc-reg-2023r03-178"
SBATCH_QOS="ehpc-reg-2023r03-178"


SBATCH_STDERR="job.%J.err"
SBATCH_STDOUT="job.%J.out"

SBATCH_MAIL_TYPE="ALL"
SBATCH_MAIL_USER="m.c.boulogne@student.utwente.nl"


if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <properties_file>"
  exit 1
fi

PROP_FILE="$1"

if [[ ! -f "$PROP_FILE" ]]; then
  echo "Properties file not found: $PROP_FILE"
  exit 1
fi

# Detect if we are inside a SLURM job or not
if [[ -z "${SLURM_JOB_ID:-}" ]]; then
  bash bash_scripts/make_mpi_params.sh "$PROP_FILE"
  # Not in SLURM: submit this script with sbatch, using SBATCH_* from the properties file

  # Absolute path to this script, independent of current working directory
  SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"

  # Load SBATCH_* variables from the properties file
  source "$PROP_FILE"

  sbatch \
    --partition="${SBATCH_PARTITION}" \
    --job-name="${SBATCH_JOB_NAME}" \
    --account="${SBATCH_ACCOUNT}" \
    --qos="${SBATCH_QOS}" \
    --time="${SBATCH_TIME}" \
    --nodes="${SBATCH_NODES}" \
    --ntasks="${SBATCH_NTASKS}" \
    --ntasks-per-core="${SBATCH_NTASKS_PER_CORE}" \
    --cpus-per-task="${SBATCH_CPUS_PER_TASK}" \
    --mem="${SBATCH_MEM}" \
    -e "${SBATCH_STDERR}" \
    -o "${SBATCH_STDOUT}" \
    --mail-type="${SBATCH_MAIL_TYPE}" \
    --mail-user="${SBATCH_MAIL_USER}" \
    --array="${SBATCH_ARRAY}" \
    "$SCRIPT_PATH" "$PROP_FILE"

  exit 0
fi

#########################################
# From here on we are inside the SLURM job #
#########################################


# Load sweep and sim parameters
source "$PROP_FILE"

# Your usual environment
source ~/.bash_shell

set -euo pipefail

# --- paths / constants ---

# If delta and MAXlevel are in the params file already, these constants are not used.
# Keep Ldomain here since your params generator didn't include it.

# Where to store outputs (change as you like)
BASE_SAVE_DIR="$PWD/Results/$SBATCH_ARRAY"

# --- select the line for this array task ---
task_id="${SLURM_ARRAY_TASK_ID}"

# Find the line whose first column equals the task id
line="$(awk -v id="$task_id" '$1==id {print; exit}' "$PARAMS_FILE")"

if [[ -z "${line}" ]]; then
  echo "ERROR: No line found for runid=$task_id in $PARAMS_FILE" >&2
  exit 1
fi

# Parse columns from the line
# Format: runid Ohd Ohf Ohe rhod rhof rhoe sigma_1 sigma_2 hf Ldomain MAXlevel delta tmax SBATCH_JOB_NAME SBATCH_TIME SBATCH_NODES TOTAL_CPUS 
read -r runid Ohd Ohf Ohe rhod rhof rhoe sigma_1 sigma_2 hf Ldomain MAXlevel delta tmax \
  SBATCH_JOB_NAME SBATCH_TIME SBATCH_NODES TOTAL_CPUS SBATCH_ARRAY <<< "$line"

savefolder="${BASE_SAVE_DIR}/{runid}"
mkdir -p "$savefolder"

echo "RunID: $runid"
echo "Params: Ohd=$Ohd Ohf=$Ohf Ohe=$Ohe rhod=$rhod rhof=$rhof rhoe=$rhoe sigma_1=$sigma_1 sigma_2=$sigma_2 hf=$hf tmax=$tmax Ldomain=$Ldomain delta=$delta MAXlevel=$MAXlevel"
echo "Savefolder: $savefolder"
echo "SLURM job: ${SLURM_JOB_ID:-NA} task: ${SLURM_ARRAY_TASK_ID:-NA}"

# save parameters to a log file
params_log="${savefolder}/parameters.txt"

{
  echo "========================"
  echo "=== Simulation info ==="
  echo "start_time = $(date -Is)"
  echo "runid = $runid"
  echo "job_id = ${SLURM_JOB_ID:-NA}"
  echo "array_task_id = ${SLURM_ARRAY_TASK_ID:-NA}"
  echo "SBATCH_NTASKS = ${SBATCH_NTASKS:-NA}"
  echo "SBATCH_CPUS_PER_TASK = ${SBATCH_CPUS_PER_TASK:-NA}"
  echo "SBATCH_NODES = ${SBATCH_NODES:-NA}"
  echo "host = $(hostname)"
  
  echo "=== Parameters ==="
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
  echo "========================"
  echo
} >> "$params_log"


# --- run ---
# Use -n to match how many MPI ranks you want.
srun -n "${SBATCH_NTASKS}" "$EXE" \
  "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
  "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder"
