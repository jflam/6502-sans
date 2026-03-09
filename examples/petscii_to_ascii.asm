; Readable PETSCII -> ASCII conversion for the common text subset.
;
; This version favors clarity over byte count. It leaves punctuation, digits,
; and control codes unchanged, but rewrites the two PETSCII alphabetic ranges
; that differ from ASCII:
;
;   $41-$5A -> $61-$7A  ; low PETSCII alpha block becomes ASCII lowercase
;   $C1-$DA -> $41-$5A  ; high PETSCII alpha block becomes ASCII uppercase
;
; Input:
;   A = one PETSCII byte
;
; Output:
;   A = ASCII byte for the common text path

petscii_to_ascii:
    CMP #$41
    BCC maybe_high_block
    CMP #$5B
    BCS maybe_high_block
    ORA #$20
    RTS

maybe_high_block:
    CMP #$C1
    BCC done
    CMP #$DB
    BCS done
    AND #$7F

done:
    RTS

; Demo wrapper: convert a NUL-terminated buffer in place through $FB/$FC.
;
; Input:
;   $FB/$FC points at the PETSCII buffer.
;
; Output:
;   The same buffer is rewritten in place as ASCII-friendly text.

petscii_buffer_to_ascii:
    LDY #$00

loop:
    LDA ($FB),Y
    BEQ buffer_done
    JSR petscii_to_ascii
    STA ($FB),Y
    INY
    BNE loop
    INC $FC
    BNE loop

buffer_done:
    RTS
