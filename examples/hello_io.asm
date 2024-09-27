section .data
message_size: 19
message: "What, is your name?"
endl: 10
hello_size: 7
hello: "Hello, "
answer_size: 0
answer: res(15)
answer_end: "!"
answer_ptr: answer


section .text
_start:
    ld message_size
    setcnt
    lda message
    setaddr
    loop_print1:
        read
        output 1
        cntz
        jz end_loop_print1
        jmp loop_print1

    end_loop_print1:
      ld endl
      output 1
      lda answer
      setaddr

    loop_write:
        input 0
        write
        cmp '\n'
        je end_write
        ld answer_size
        inc
        st answer_size
        ld answer_ptr
        add 4
        st answer_ptr
        setaddr
        jmp loop_write

    end_write:

    ld hello_size
    setcnt
    lda hello
    setaddr
    loop_print2:
        read
        output 1
        cntz
        jz loop_print2_end
        jmp loop_print2

    loop_print2_end:

    ld answer_size
    setcnt
    lda answer
    setaddr
    loop_print3:
        read
        output 1
        cntz
        jz print_answer_end
        jmp loop_print3

    print_answer_end:
        ld answer_end
        output 1
    exit:
        hlt