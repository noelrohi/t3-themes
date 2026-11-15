#!/bin/sh
# Rebuild each theme's CSS from sources/<theme>/combo.py into themes/<theme>.json, then install.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
for dir in "$root"/sources/*/; do
  name="$(basename "$dir")"
  [ -f "$dir/combo.py" ] && [ -f "$root/themes/$name.json" ] || continue
  python3 -I "$dir/combo.py" "$dir" >/dev/null
  python3 -I - "$root/themes/$name.json" "$dir/combo.css" <<'PY'
import json, sys
theme_path, css_path = sys.argv[1], sys.argv[2]
theme = json.load(open(theme_path))
theme["css"] = open(css_path).read()
if len(theme["css"]) > 20000:
    sys.exit(f"{theme_path}: css is {len(theme['css'])} chars, over T3's 20000 limit")
json.dump(theme, open(theme_path, "w"), indent=2)
print(f"built {theme_path} ({len(theme['css'])} css chars)")
PY
done
"$root/scripts/install.sh"
