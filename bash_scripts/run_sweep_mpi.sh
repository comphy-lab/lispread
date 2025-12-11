#!/bin/bash
set -euo pipefail

# Usage:
#   ./sweep_job_mpi.sh sweep_properties.sh

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <properties_file>"
  exit 1
fi

PROP_FILE="$1"

if [[ ! -f "$PROP_FILE" ]]; then
  echo "Properties file not found: $PROP_FILE"
  exit 1
fi

# Outside SLURM -> submit ourselves
if [[ -z "${SLURM_JOB_ID:-}" ]]; then
  here="$(dirname "$0")"
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
    "${here}/$(basename "$0")" "$PROP_FILE"

  exit 0
fi

# Inside SLURM job
source "$PROP_FILE"
source ~/.bash_shell

run_one() {
  local Ohd="$1" Ohf="$2" Ohe="$3" sigma_1="$4" sigma_2="$5" MAXlevel="$6" hf="$7" tmax="$8" id="$9"

  local tag="${id}_\
Ohd_${Ohd}_Ohf_${Ohf}_Ohe_${Ohe}_\
rho_d_${rhod}_rho_f_${rhof}_rho_e_${rhoe}_\
s1_${sigma_1}_s2_${sigma_2}_\
hf_${hf}_Ldomain_${Ldomain}_delta_${delta}_MaxLevel_${MAXlevel}"

  local folder_tag="${tag//./p}"
  local savefolder="Results/${sub_save_folder}${folder_tag}"
  mkdir -p -- "$savefolder"

  (
    set -e

    # Use OpenMPI for threading over space / domain, etc
    mpirun -np "${THREADS_PER_SIM}" ./bubbleAtLubis \
      "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
      "$sigma_1" "$sigma_2" "$hf" "$tmax" "$Ldomain" "$delta" "$MAXlevel" "$savefolder" \
      > "${savefolder}/logTerminal" 2>&1
  ) &
}

wait_for_slot() {
  while (( $(jobs -rp | wc -l) >= MAX_PAR )); do
    wait -n
  done
}

id_counter=$id_start

for MAXlevel in "${MAXlevel_list[@]}"; do
  for i in "${!Ohf_list[@]}"; do
    Ohf="${Ohf_list[$i]}"
    tmax="${tmax_list[$i]}"
    for Ohd in "${Ohd_list[@]}"; do
      for hf in "${hf_list[@]}"; do
        for Ohe in "${Ohe_list[@]}"; do
          for sigma_1 in "${sigma1_list[@]}"; do
            for sigma_2 in "${sigma2_list[@]}"; do
              wait_for_slot
              run_one "$Ohd" "$Ohf" "$Ohe" "$sigma_1" "$sigma_2" "$MAXlevel" "$hf" "$tmax" "$id_counter"
              id_counter=$((id_counter + 1))
            done
          done
        done
      done
    done
  done
done

wait
