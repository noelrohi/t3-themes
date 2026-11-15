#!/bin/sh
# Search T3 Code's bundled UI code for a string (an attribute, class, or visible text).
# Usage: scripts/find-selector.sh 'data-chat-header' [chars of context, default 300]
set -eu
pattern="$1"; ctx="${2:-300}"
app="/Applications/T3 Code (Nightly).app"
version="$(defaults read "$app/Contents/Info" CFBundleShortVersionString)"
cache="${TMPDIR:-/tmp}/t3-asar/$version"
if [ ! -d "$cache" ]; then
  mkdir -p "$cache"
  npx -y @electron/asar extract "$app/Contents/Resources/app.asar" "$cache" >/dev/null
fi
grep -oh ".\{0,$ctx\}$pattern.\{0,$ctx\}" "$cache"/apps/server/dist/client/assets/*.js
