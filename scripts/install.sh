#!/bin/sh
# Copy every theme in themes/ into T3 Code's theme folder.
set -eu
dest="$HOME/.t3/userdata/themes"
mkdir -p "$dest"
cd "$(dirname "$0")/../themes"
for f in *.json; do
  cp "$f" "$dest/$f"
  echo "installed $f"
done
