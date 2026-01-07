#!/bin/bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <parameter_file>" >&2
  exit 1
fi

param_file="$1"

if [ ! -f "$param_file" ]; then
  echo "Parameter file not found: $param_file" >&2
  exit 1
fi

source "$param_file"


: > "$PARAMS_FILE"
printf "# runid Ohd Ohf Ohe rhod rhof rhoe sigma1 sigma2 hf Ldomain MAXlevel delta tmax SBATCH_JOB_NAME SBATCH_TIME SBATCH_NODES TOTAL_CPUS SBATCH_ARRAY\n" > "$PARAMS_FILE"

runid=$((id_start))   # starting run ID

for MAXlevel in "${MAXlevel_list[@]}"; do
  for i in "${!Ohf_list[@]}"; do
    Ohf="${Ohf_list[$i]}"
    tmax="${tmax_list[$i]}"
    for Ohd in "${Ohd_list[@]}"; do
      for hf in "${hf_list[@]}"; do
        for Ohe in "${Ohe_list[@]}"; do
          for sigma1 in "${sigma1_list[@]}"; do
            for sigma2 in "${sigma2_list[@]}"; do
            
            printf "%d %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" \
              "$runid" "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" \
              "$sigma1" "$sigma2" "$hf" "$Ldomain" "$MAXlevel" "$delta" "$tmax" \
              "$SBATCH_JOB_NAME" "$SBATCH_TIME" "$SBATCH_NODES" "0" "$SBATCH_ARRAY">> "$PARAMS_FILE"

              runid=$((runid+1))
            done
          done
        done
      done
    done
  done
done


if [ "$runid" -ne $((id_end + 1)) ]; then
  echo "ERROR: runid ended at $((runid-1)), expected $id_end" >&2
  exit 1
fi
