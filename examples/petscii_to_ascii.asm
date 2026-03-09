; PETSCII -> ASCII fast path.
;
; Input:
;   A holds one PETSCII byte.
;
; Output:
;   A holds the ASCII byte for the common printable-text path.
;
; Caveats:
;   The caller handles the NUL terminator before calling this helper.
;   This is the code-golfed path, so control codes and '@' are out of scope.
;
; Trick:
;   $20-$3F already have bit 5 set, so ORA #$20 is a no-op there and only
;   changes $41-$5A into ASCII lowercase. The high PETSCII letter block is the
;   same letters with bit 7 set, so BMI + AND #$7F folds it to ASCII uppercase.

petscii_to_ascii_fast:
    BMI high_block
    CMP #$5B
    BCS done
    ORA #$20
done:
    RTS

high_block:
    AND #$7F
    RTS

; Demo wrapper: convert a NUL-terminated buffer in place through $FB/$FC.

petscii_buffer_to_ascii:
    LDY #$00

loop:
    LDA ($FB),Y
    BEQ buffer_done
    JSR petscii_to_ascii_fast
    STA ($FB),Y
    INY
    BNE loop
    INC $FC
    BNE loop

buffer_done:
    RTS
