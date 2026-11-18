#!/bin/bash
# Render every job in cad/render/jobs into assets/renders. Run from anywhere.
cd "$(dirname "$0")/../.."
BL=${BLENDER:-blender}
[ -x "/Applications/Blender.app/Contents/MacOS/Blender" ] && BL="/Applications/Blender.app/Contents/MacOS/Blender"
for j in cad/render/jobs/${1:-*}.json; do echo "== $j"; "$BL" -b -P cad/render/render.py -- "$j" | grep -E "WROTE|SCREENRECT|Error"; done
