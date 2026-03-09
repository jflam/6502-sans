#!/usr/bin/env python3

"""Generate the documented MOS 6502 opcode table used by the font generator.

Source table: py65's MPU.disassemble list.
"""

from __future__ import annotations

import json
from pathlib import Path

from py65.devices.mpu6502 import MPU


DISASM_TEMPLATES = {
    "imp": "{mnemonic}",
    "acc": "{mnemonic} A",
    "imm": "{mnemonic} #$n",
    "zpg": "{mnemonic} <$n",
    "zpx": "{mnemonic} <$n,X",
    "zpy": "{mnemonic} <$n,Y",
    "abs": "{mnemonic} $nn",
    "abx": "{mnemonic} $nn,X",
    "aby": "{mnemonic} $nn,Y",
    "ind": "{mnemonic} ($nn)",
    "inx": "{mnemonic} ($n,X)",
    "iny": "{mnemonic} ($n),Y",
    "rel": "{mnemonic} *o",
}

ENCODING_SUFFIXES = {
    "imp": "",
    "acc": "",
    "imm": " n",
    "zpg": " n",
    "zpx": " n",
    "zpy": " n",
    "abs": " nn nn",
    "abx": " nn nn",
    "aby": " nn nn",
    "ind": " nn nn",
    "inx": " n",
    "iny": " n",
    "rel": " o",
}


def build_entries() -> list[list[str]]:
    entries: list[list[str]] = []
    for opcode, (mnemonic, mode) in enumerate(MPU.disassemble):
        if mnemonic == "???":
            continue
        if mode not in DISASM_TEMPLATES:
            raise ValueError(f"Unsupported addressing mode: {mode}")
        disasm = DISASM_TEMPLATES[mode].format(mnemonic=mnemonic)
        encoding = f"{opcode:02X}{ENCODING_SUFFIXES[mode]}"
        entries.append([disasm, encoding])
    return entries


def main() -> None:
    output_path = Path("resources/instructions.json")
    output_path.write_text(json.dumps(build_entries(), indent=2) + "\n")


if __name__ == "__main__":
    main()
