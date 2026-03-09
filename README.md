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

One short Commodore 64-flavored example is a tiny `CHROUT` routine that clears the screen, switches to light blue text, prints `C64`, and returns:

```text
A99320D2FFA99A20D2FFA94320D2FFA93620D2FFA93420D2FF60
```

That shapes into:

```asm
LDA #$93
JSR $FFD2
LDA #$9A
JSR $FFD2
LDA #$43
JSR $FFD2
LDA #$36
JSR $FFD2
LDA #$34
JSR $FFD2
RTS
```

On a C64, `CHROUT` lives at `$FFD2`, `$93` is the clear-screen PETSCII control code, and `$9A` selects light blue text.

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

The generated `.ttf` is copied to `~/.local/share/fonts/` and can also be found at `./test/6502-sans.ttf`.

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

## License

- Droid Sans Mono is under [Apache Licence](./LICENSE.Apache.txt)
- Noto Sans Mono is under [Open Font License](./LICENSE.OFL.txt)
- This fork's source changes are under [MIT License](./LICENSE.txt)
