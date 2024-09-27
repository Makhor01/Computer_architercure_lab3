section .data
fib1: 1
fib2: 2
sum: 0
temp: 0
limit: 4000000

section .text
_start:
    ld fib1
    st temp
    ld fib2
    st fib1
    ld temp
    st fib2
    ld limit
    st temp

loop:
    ld fib1
    add fib2
    st temp
    ld temp
    cmp limit
    jge exit
    ld temp
    mod 2
    jz add_to_sum
    ld fib2
    st fib1
    ld temp
    st fib2
    jmp loop

add_to_sum:
    ld sum
    add temp
    st sum
    ld fib2
    st fib1
    ld temp
    st fib2
    jmp loop
exit:
    ld sum
    output 1
    hlt