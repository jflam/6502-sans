#!/usr/bin/env fontforge -lang=py -script

import os
import sys
from pathlib import Path
import math

import fontforge
import psMat


FONT_NAME = "6502 Sans"
POSTSCRIPT_NAME = "6502Sans"
PRIVATE_USE_START = 0xE000
IMPORTED_GLYPH_YMIN = 728.0
IMPORTED_GLYPH_YMAX = 789.0
OFFSET_LSB = 0
OFFSET_ADVANCE = 460


def import_svg_glyphs(font, svg_dir, target_height, offset_lsb, offset_advance):
    codepoint = PRIVATE_USE_START
    for svg_path in sorted(svg_dir.glob("*.svg")):
        glyph = font.createChar(codepoint, svg_path.stem)
        glyph.importOutlines(str(svg_path), correctdir=False, scale=False)
        glyph.transform(psMat.translate(0, -IMPORTED_GLYPH_YMIN))
        glyph.transform(
            psMat.scale(target_height / (IMPORTED_GLYPH_YMAX - IMPORTED_GLYPH_YMIN))
        )
        x_min, _, x_max, _ = glyph.boundingBox()
        if glyph.glyphname.startswith("offset_"):
            glyph.transform(psMat.translate(offset_lsb - x_min, 0))
            glyph.width = offset_advance
        else:
            glyph.transform(psMat.translate(-x_min, 0))
            glyph.width = math.ceil(x_max - x_min)
        glyph.round()
        codepoint += 1


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_font.py <svg_dir> <output_ttf>")

    svg_dir = Path(sys.argv[1]).resolve()
    output_ttf = Path(sys.argv[2]).resolve()
    base_ttf = Path("resources/NotoSansMono-Regular.ttf").resolve()

    output_ttf.parent.mkdir(parents=True, exist_ok=True)
    os.makedirs(Path.home() / ".config" / "fontforge" / "plugin", exist_ok=True)

    font = fontforge.open(str(base_ttf))
    font.fontname = POSTSCRIPT_NAME
    font.familyname = FONT_NAME
    font.fullname = FONT_NAME
    font.autoWidth(0, 0, 2500)
    cap_bbox = font["A"].boundingBox()
    target_height = cap_bbox[3] - cap_bbox[1]
    import_svg_glyphs(font, svg_dir, target_height, OFFSET_LSB, OFFSET_ADVANCE)
    font.generate(str(output_ttf))


if __name__ == "__main__":
    main()
