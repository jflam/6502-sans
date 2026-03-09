#!/usr/bin/env python3

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from fontTools.ttLib import TTFont


RELEASE_VERSION = "1.0"
FONT_REVISION = 1.0
FONT_VERSION_STRING = "Version 1.000"
FAMILY_NAME = "6502 Sans"
SUBFAMILY_NAME = "Regular"
FULL_NAME = f"{FAMILY_NAME} {SUBFAMILY_NAME}"
POSTSCRIPT_NAME = "6502Sans-Regular"
UNIQUE_ID = f"1.000;jflam;{POSTSCRIPT_NAME}"
COPYRIGHT = (
    "Portions copyright 2015 Google LLC. "
    "6502 Sans modifications copyright 2026 jflam."
)
MANUFACTURER = "jflam"
DESIGNER = "Monotype Design Team; 6502 adaptation by jflam"
DESCRIPTION = (
    "MOS 6502-flavored fork of z80-sans. "
    "Release engineering attribution: gpt-5.4/xhigh."
)
REPO_URL = "https://github.com/jflam/6502-sans"


def set_name_records(font: TTFont) -> None:
    name_table = font["name"]
    license_record = name_table.getDebugName(13) or ""
    license_url = name_table.getDebugName(14) or ""

    name_table.names = []
    for platform_id, plat_enc_id, lang_id in ((3, 1, 0x409), (1, 0, 0x0)):
        name_table.setName(COPYRIGHT, 0, platform_id, plat_enc_id, lang_id)
        name_table.setName(FAMILY_NAME, 1, platform_id, plat_enc_id, lang_id)
        name_table.setName(SUBFAMILY_NAME, 2, platform_id, plat_enc_id, lang_id)
        name_table.setName(UNIQUE_ID, 3, platform_id, plat_enc_id, lang_id)
        name_table.setName(FULL_NAME, 4, platform_id, plat_enc_id, lang_id)
        name_table.setName(FONT_VERSION_STRING, 5, platform_id, plat_enc_id, lang_id)
        name_table.setName(POSTSCRIPT_NAME, 6, platform_id, plat_enc_id, lang_id)
        name_table.setName(MANUFACTURER, 8, platform_id, plat_enc_id, lang_id)
        name_table.setName(DESIGNER, 9, platform_id, plat_enc_id, lang_id)
        name_table.setName(DESCRIPTION, 10, platform_id, plat_enc_id, lang_id)
        name_table.setName(REPO_URL, 11, platform_id, plat_enc_id, lang_id)
        name_table.setName(REPO_URL, 12, platform_id, plat_enc_id, lang_id)
        name_table.setName(license_record, 13, platform_id, plat_enc_id, lang_id)
        name_table.setName(license_url, 14, platform_id, plat_enc_id, lang_id)
        name_table.setName(FAMILY_NAME, 16, platform_id, plat_enc_id, lang_id)
        name_table.setName(SUBFAMILY_NAME, 17, platform_id, plat_enc_id, lang_id)


def finalize_font(input_ttf: Path, stable_output_ttf: Path) -> None:
    stable_output_ttf.parent.mkdir(parents=True, exist_ok=True)

    font = TTFont(input_ttf)
    font["head"].fontRevision = FONT_REVISION
    set_name_records(font)
    font.save(input_ttf)
    font.close()

    shutil.copy2(input_ttf, stable_output_ttf)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: finalize_font.py <input_ttf> <stable_output_ttf>")

    input_ttf = Path(sys.argv[1]).resolve()
    stable_output_ttf = Path(sys.argv[2]).resolve()
    finalize_font(input_ttf, stable_output_ttf)
    print(f"Finalized {input_ttf.name} as {FAMILY_NAME} {RELEASE_VERSION}")


if __name__ == "__main__":
    main()
