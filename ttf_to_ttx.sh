#!/bin/sh

set -eux

repo_root="$PWD"

rm -f .fontcustom-manifest.json
mkdir -p ./fontcustom
rm -f ./fontcustom/fontcustom_*.ttf ./fontcustom/fontcustom_*.ttx
fontforge -lang=py -script ./scripts/build_font.py ./out_svg/ ./fontcustom/fontcustom_6502.ttf

cd ./fontcustom
last_ttf=$(find . -iname 'fontcustom_*.ttf' -print0 | xargs -r -0 ls -1 -t | head -1)
"$repo_root/.venv/bin/python" -m fontTools.ttx "$last_ttf"
