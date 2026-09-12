#!/usr/bin/env bash
set -euo pipefail

folder="${1:-.}"
prefix="${2:-file}"
count=1

find "$folder" -maxdepth 1 -type f | sort | while read -r file; do
  ext="${file##*.}"
  printf 'PREVIEW: %s -> %s_%03d.%s\n' "$file" "$prefix" "$count" "$ext"
  count=$((count + 1))
done

echo "Preview only. No files were renamed."
