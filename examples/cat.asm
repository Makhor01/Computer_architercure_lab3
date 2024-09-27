section .data

section .text
_start:
    loop:
        input 0
        cmp '\n'
        je exit
        output 1
        jmp loop
    exit:
        hlt