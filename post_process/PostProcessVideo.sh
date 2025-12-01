#!/bin/bash
# Run post-processing for all simulation subdirectories inside a given directory
# Usage: ./postprocess_all.sh /path/to/parent_directory_with_subdirs

set -euo pipefail

# ---------- Config ----------
MAX_PAR=4           # Max number of concurrent postprocessing tasks
THREADS_PER_SIM=1   # Threads per Python postprocessing

# ---------- Check input ----------
if [[ $# -ne 1 ]]; then
  echo "Error"
  exit 1
fi

PARENT_DIR="$1"

if [[ ! -d "$PARENT_DIR" ]]; then
  echo "Error: directory '$PARENT_DIR' does not exist."
  exit 1
fi

# ---------- Function to process a single simulation folder ----------
run_postprocessing() {
  local folder="$1"
  echo "Processing folder: $folder"

  # Extract parameters from folder name if possible
  local tag
  tag=$(basename "$folder")

  # Try to extract Ldomain and hf from the folder name
  # e.g., 2025_09_30_Ohd_4p6e-3_Ldomain_10.0_Ohf_2.5
  local Ldomain hf Ohf
  Ldomain=$(echo "$tag" | grep -oP '(?<=Ldomain_)[0-9p.-]+' || true)

  # Extract hf value
  hf=$(echo "$tag" | grep -oP '(?<=_hf_)[0-9p.-]+' || true)

  # Ensure `p` is replaced with `.` for proper number formatting
  hf=$(echo "$hf" | sed 's/p/./g')

  # get Ohnesorge numbers
  Ohd=$(echo "$tag" | grep -oP '(?<=Ohd_)[0-9p.e+-]+' || true)
  Ohf=$(echo "$tag" | grep -oP '(?<=Ohf_)[0-9p.e+-]+' || true)
  Ohe=$(echo "$tag" | grep -oP '(?<=Ohe_)[0-9p.e+-]+' || true)

  # p vervangen door punt
  Ohd=$(echo "$Ohd" | sed 's/p/./g')
  Ohf=$(echo "$Ohf" | sed 's/p/./g')
  Ohe=$(echo "$Ohe" | sed 's/p/./g')



  echo "  → Ldomain=$Ldomain, hf=$hf, Ohd=$Ohd, Ohf=$Ohf, Ohe=$Ohe"

  # Run post-processing (redirect output)
  (
    set -e
    export OMP_NUM_THREADS="${THREADS_PER_SIM}"

    {
      python3 Video.py "$hf" "$Ldomain" "$Ohd" "$Ohf" "$Ohe" "$folder" 
    } > "${folder}/logVideoPostProccessing" 2>&1

  #   # Make movie if tracking images exist
    if [[ -d "${folder}/Video" ]]; then
      (
        cd "$folder"
        ffmpeg -y -framerate 60 -pattern_type glob -i 'Video/*.png' \
                   -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4 \
                       > ffmpeg_video.log 2>&1 || true
      )
    fi
  ) &

}

# ---------- Concurrency limiter ----------
wait_for_slot() {
  while (( $(jobs -rp | wc -l) >= MAX_PAR )); do
    wait -n
  done
}

# ---------- Main loop ----------
echo "Scanning parent directory: $PARENT_DIR"
for folder in "$PARENT_DIR"/*; do
  if [[ -d "$folder" ]]; then
    wait_for_slot
    run_postprocessing "$folder"
  fi
done

wait
echo "✅ All post-processing tasks completed."
