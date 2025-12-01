#!/bin/bash
# Usage: ./RunAllPostProcess.sh dir1 dir2 dir3 ...

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Error: you must provide at least one directory."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
POSTPROCESS_SCRIPT="PostProcessVideo.sh"

if [[ ! -f "$POSTPROCESS_SCRIPT" ]]; then
  echo "Error: PostProcessVideo.sh not found in the same directory."
  exit 1
fi

for target in "$@"; do
  if [[ -d "$target" ]]; then
    echo "Running PostProcess.sh for $target"
    bash PostProcessVideo.sh "$target"
  else
    echo "Skipping $target because it is not a directory"
  fi
done

echo "All directories processed."