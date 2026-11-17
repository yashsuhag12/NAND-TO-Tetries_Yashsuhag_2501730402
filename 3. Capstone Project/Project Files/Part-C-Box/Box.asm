// K = 23. Box starts at row 23, is 20 rows high and 64 pixels (4 words) wide.
// Draw black while a key is pressed; erase to white when no key is pressed.
// Each screen row contains 32 words. Start = SCREEN + 32*23 = 17120.

(START)
    @17120
    D=A
    @R13
    M=D
    @20
    D=A
    @R14
    M=D

(FRAME)
    // Choose black (-1) if a key is pressed, otherwise white (0).
    @KBD
    D=M
    @BLACK
    D;JNE
    @WHITE
    0;JMP

(BLACK)
    @R12
    M=-1
    @DRAW
    0;JMP

(WHITE)
    @R12
    M=0

(DRAW)
    @R13
    D=M
    @R15
    M=D
    @4
    D=A
    @R11
    M=D

(WORD_LOOP)
    @R12
    D=M
    @R15
    A=M
    M=D
    @R15
    M=M+1
    @R11
    M=M-1
    D=M
    @WORD_LOOP
    D;JGT

    // Move pointer from the end of this 4-word strip to next screen row (+28).
    @R13
    D=M
    @4
    D=D+A
    @28
    D=D+A
    @R13
    M=D

    @R14
    M=M-1
    D=M
    @FRAME
    D;JGT

    // Repeat continuously so key state is polled again.
    @START
    0;JMP
