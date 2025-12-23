#!/bin/bash

# Base parameters (shared across runs)
rhoe="1"
rhof="0.9"
rhod="1.2e-3"
Ldomain="5"
delta="0.01"

# Parameter sweeps
Ohe_list=( "5.0e-3" "2.5e-2" )
Ohf_list=( "10" "20" "30" "40" )
tmax_list=( "1" "1.5" "2.5" "2.5" )
Ohd_list=( "9.1e-5" )
sigma2_list=( "0.33" )
sigma1_list=( "0.67" )
MAXlevel_list=( "10" )
hf_list=( "0.03" "0.05" )

id_start="2500"
id_end="2515"
out="bash_scripts/mpi_params/params_${id_start}_to_${id_end}_start.txt"

: > "$out"

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

              printf "%d %s %s %s %s %s %s %s %s %s %s %s %s %s\n" "$runid" "$Ohd" "$Ohf" "$Ohe" "$rhod" "$rhof" "$rhoe" "$sigma1" "$sigma2" "$hf" "$Ldomain" "$MAXlevel" "$delta" "$tmax" >> "$out"

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
