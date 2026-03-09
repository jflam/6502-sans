; Golfed PETSCII -> ASCII fast path.
;
; This is the compact printable-text helper used in the README demo.
; It assumes the caller already filtered out the NUL terminator and does
; not try to preserve PETSCII control semantics outside the common text path.
;
; Trick:
;   $20-$3F already have ASCII bit 5 set, so ORA #$20 only changes $41-$5A.
;   The high PETSCII alpha block is the same letters with bit 7 set, so
;   AND #$7F folds $C1-$DA back to ASCII uppercase.
;
; Input:
;   A = one PETSCII byte
;
; Output:
;   A = ASCII byte for the common printable-text path

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
