#!/bin/sh
# Screenshot T3 Code's main window, even when it is behind other apps.
# Usage: scripts/shot.sh [out.png]   -> writes out.png and a 1600px-wide out-small.png
set -eu
out="${1:-${TMPDIR:-/tmp}/t3-shot.png}"
id="$(swift - <<'SWIFT'
import CoreGraphics
let wins = CGWindowListCopyWindowInfo([.optionAll], kCGNullWindowID) as! [[String: Any]]
var best = (0, 0.0)
for w in wins where (w["kCGWindowOwnerName"] as? String ?? "").hasPrefix("T3 Code") && (w["kCGWindowLayer"] as? Int ?? 1) == 0 {
  let b = w["kCGWindowBounds"] as! [String: Double]
  let area = (b["Width"] ?? 0) * (b["Height"] ?? 0)
  if area > best.1 { best = (w["kCGWindowNumber"] as! Int, area) }
}
print(best.0)
SWIFT
)"
[ "$id" != 0 ] || { echo "T3 Code window not found" >&2; exit 1; }
screencapture -x -o -l "$id" "$out"
small="${out%.png}-small.png"
sips -Z 1600 "$out" --out "$small" >/dev/null
echo "$small"
