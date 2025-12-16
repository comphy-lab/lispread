#!/bin/bash
# Run post-processing for all simulation subdirectories inside a given directory
# Usage: ./postprocess_all.sh /path/to/parent_directory_with_subdirs

set -euo pipefail

# ---------- Config ----------
MAX_PAR=16           # Max number of concurrent postprocessing tasks
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

  echo "  → Ldomain=$Ldomain, hf=$hf"

  # Run post-processing (redirect output)
  (
    set -e
    export OMP_NUM_THREADS="${THREADS_PER_SIM}"

    {
      python3 -u TriplePointWithBubblesEntrapped.py "0" "$Ldomain" "$hf" "$folder"
      # Add other postprocess scripts as needed
      # python3 Video.py "$hf" "$Ldomain" ...
    } > "${folder}/logTriplePointPostProccessingWithEntrapped" 2>&1

  #   # Make movie if tracking images exist
    if [[ -d "${folder}/TrackingTPWithBubblesEntrapped" ]]; then
      (
        cd "$folder"
        ffmpeg -y -framerate 60 -pattern_type glob -i 'TrackingTPWithBubblesEntrapped/*.png' \
          -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" \
          -c:v libx264 -r 30 -pix_fmt yuv420p TPsimEntrapped.mp4 \
          > ffmpeg_TP.log 2>&1 || true
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
