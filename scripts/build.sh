#!/bin/sh
# Build every theme from bases/ + sources/<id>/ into themes/<id>.json, then install. See scripts/build.py.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
python3 -I "$root/scripts/build.py"
"$root/scripts/install.sh"
