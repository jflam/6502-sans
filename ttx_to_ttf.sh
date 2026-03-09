#!/bin/sh

set -eux

repo_root="$PWD"

cd ./fontcustom
rm -f fontcustom_*.ttf
last_ttx=$(find . -iname 'fontcustom_*.ttx' -print0 | xargs -r -0 ls -1 -t | head -1)
"$repo_root/.venv/bin/python" -m fontTools.ttx "$last_ttx"

rm -f ~/.local/share/fonts/fontcustom_*.ttf
last_ttf=$(find . -iname 'fontcustom_*.ttf' -print0 | xargs -r -0 ls -1 -t | head -1)
"$repo_root/.venv/bin/python" "$repo_root/scripts/finalize_font.py" \
  "$PWD/$last_ttf" \
  "$repo_root/test/6502-sans.ttf"
"$repo_root/.venv/bin/python" -m fontTools.ttx -q -o "$last_ttx" "$last_ttf"
cp "$last_ttf" ~/.local/share/fonts/
