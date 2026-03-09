# 6502 Sans

A MOS 6502-flavored fork of [nevesnunes/z80-sans](https://github.com/nevesnunes/z80-sans).

Type hexadecimal bytes into an OpenType-aware editor and watch them reshape live into disassembled 6502 instructions. The generated font is available at `./test/6502-sans.ttf`, with a quick preview at `./test/6502-sans-sample.png`.

## What It Covers

- Documented NMOS 6502 opcodes only: 151 instructions.
- 6502-style assembly syntax:
  - immediates as `#$nn`
  - zero-page and absolute addresses as `<$nn` / `$nnnn`
  - indexed and indirect forms like `($nn,X)`, `($nn),Y`, `$nnnn,X`
  - relative branches rendered as `*+nn` / `*-nn`
- Uppercase and lowercase hexadecimal input.

## Live Typing

This is especially fun in TextEdit: select `6502 Sans`, start typing hex bytes, and the font rewrites them on screen as you go.

A better code-golf demo than a straight `CHROUT` loop is the 12-byte PETSCII-to-ASCII fast path in [`examples/petscii_to_ascii_fast.asm`](./examples/petscii_to_ascii_fast.asm). It assumes the caller already handled the NUL terminator and targets the common printable-text path. The trick is that `$20-$3F` already have ASCII bit 5 set, so `ORA #$20` only changes `$41-$5A`, while the high PETSCII letter block is just the same letters with bit 7 set and collapses with `AND #$7F`.

```text
3007
C95B
B002j
0920
60
297F
60
```

That shapes into:

```asm
BMI *+07
CMP #$5B
BCS *+02
ORA #$20
RTS
AND #$7F
RTS
```

For the readable, less optimized version with an in-place `$FB/$FC` buffer walker, see [`examples/petscii_to_ascii.asm`](./examples/petscii_to_ascii.asm). The golfed fast path above lives in [`examples/petscii_to_ascii_fast.asm`](./examples/petscii_to_ascii_fast.asm).

## Build

On macOS, install the native font tools with Homebrew:

```sh
brew install fontforge potrace woff2
python3 -m venv .venv
./.venv/bin/pip install beautifulsoup4 fonttools lxml py65
```

Then generate the instruction table and build the font:

```sh
./.venv/bin/python scripts/generate_6502_instructions.py
./.venv/bin/python gen.py ./resources/instructions.json
```

The generated `.ttf` is copied to `~/.local/share/fonts/` and also written to `./test/6502-sans.ttf`.

## Notes

- This repo is a direct 6502 adaptation of [nevesnunes/z80-sans](https://github.com/nevesnunes/z80-sans). The disassembler-font idea, the GSUB/GPOS-driven lookup graph, and the original generator structure all come from that project.
- The opcode table is generated from [`py65`](https://github.com/mnaberez/py65)'s built-in 6502 disassembly table instead of being hand-maintained.
- This fork replaces the original Ruby/fontcustom step with a direct FontForge import script in `scripts/build_font.py`.
- The generator still uses the original approach of rendering literal instruction fragments to SVG and injecting GSUB/GPOS tables into a mono base font.
- Zero-page modes are rendered with a leading `<` to disambiguate them from absolute modes inside the GSUB lookup graph.

## Polish In This Fork

- Uppercase input `A-F` is normalized, and rendered hex output is uppercase.
- Hex digits and addresses were respaced so byte streams read as tighter groups.
- The `$` prefix now sits flush against hex values instead of floating with a mono gap.
- Mnemonic fragments were retuned for cleaner visual spacing.

## Quick Checks

These sample byte streams shape as expected with `hb-shape`:

- `A900` -> `LDA #$00`
- `85FF` -> `STA <$FF`
- `8D0200` -> `STA $0002`
- `4C3412` -> `JMP $1234`
- `D0FE` -> `BNE *-02`

## Credits

- Original concept, Z80 version, and generator architecture: [nevesnunes/z80-sans](https://github.com/nevesnunes/z80-sans)
- Base fonts: Droid Sans Mono and Noto Sans Mono
- 6502 opcode source: [`py65`](https://github.com/mnaberez/py65)
- Release engineering attribution: `gpt-5.4/xhigh`

## License

- Droid Sans Mono is under [Apache Licence](./LICENSE.Apache.txt)
- Noto Sans Mono is under [Open Font License](./LICENSE.OFL.txt)
- This fork's source changes are under [MIT License](./LICENSE.txt)
