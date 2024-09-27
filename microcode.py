from enum import Enum

from isa import Opcode


class Signal(Enum):
    LATCH_PM = 1

    SEL_MPC_ZERO = 1 << 1
    SEL_MPC_OPC = 1 << 1 | 1 << 2
    SEL_MPC_INC = 1 << 1 | 1 << 3

    LATCH_MC = 1 << 4

    SEL_PC_NEXT = 1 << 5
    SEL_JMP = 1 << 5 | 1 << 8
    SEL_JZ = 1 << 5 | 1 << 7
    SEL_JE = 1 << 5 | 1 << 7 | 1 << 8
    SEL_JGE = 1 << 5 | 1 << 6

    SEL_AR_NEXT = 1 << 9
    SEL_AR_ADDR = 1 << 9 | 1 << 11
    SEL_AR_ACC = 1 << 9 | 1 << 10

    LATCH_DATA_MEM = 1 << 12

    SEL_ACC_DATA_MEM = 1 << 13
    SEL_ACC_IO = 1 << 13 | 1 << 15
    SEL_ACC_VAL = 1 << 13 | 1 << 14

    LATCH_WRITE_IO = 1 << 16
    LATCH_BUFF = 1 << 17

    # 17 bit: flag, 18-20 bits: operations
    SEL_ALU_INC = 1 << 18
    SEL_ALU_DEC = 1 << 18 | 1 << 21
    SEL_ALU_ADD = 1 << 18 | 1 << 20
    SEL_ALU_SUB = 1 << 18 | 1 << 20 | 1 << 21
    SEL_ALU_MUL = 1 << 18 | 1 << 19
    SEL_ALU_DIV = 1 << 18 | 1 << 19 | 1 << 21
    SEL_ALU_MOD = 1 << 18 | 1 << 19 | 1 << 20

    SEL_DC_DEC = 1 << 22
    SEL_DC_ACC = 1 << 22 | 1 << 23

    SEL_CMP_ACC = 1 << 24
    SEL_CMP_DC = 1 << 24 | 1 << 25

    HLT = 1 << 26

    def __str__(self):
        return str(self.value)


# Объединенные микроинструкции
microinstructions = [
    # ld 0
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value,  # sel_ar_addr
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_PC_NEXT.value,  # sel_acc_data_mem, sel_pc_next
    # st 3
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value,  # sel_ar_addr
    Signal.LATCH_DATA_MEM.value | Signal.SEL_PC_NEXT.value,  # latch_data_mem, sel_pc_next
    # lda 6
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ACC_VAL.value | Signal.SEL_PC_NEXT.value,  # sel_acc_val, sel_pc_next
    # write 8
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_DATA_MEM.value | Signal.SEL_DC_DEC.value,  # latch_data_mem, sel_dc_dec
    Signal.SEL_AR_NEXT.value | Signal.SEL_PC_NEXT.value,  # sel_ar_next, sel_pc_next
    # read 11
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_DC_DEC.value,  # latch_data_mem, sel_dc_dec
    Signal.SEL_AR_NEXT.value | Signal.SEL_PC_NEXT.value,  # sel_ar_next, sel_pc_next
    # setcnt 14
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_DC_ACC.value | Signal.SEL_PC_NEXT.value,  # sel_dc_acc, sel_pc_next
    # setaddr 16
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ACC.value | Signal.SEL_PC_NEXT.value,  # sel_ar_addr, sel_pc_next
    # jmp 18
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JMP.value,  # sel_jmp
    # jz 20
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JZ.value,  # sel_jz
    # jge 22
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JGE.value,  # sel_jge
    # je 24
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JE.value,  # sel_je
    # inc 26
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ALU_INC.value | Signal.SEL_PC_NEXT.value,  # sel_alu_inc, sel_pc_next
    # dec 28
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ALU_DEC.value | Signal.SEL_PC_NEXT.value,  # sel_alu_dec, sel_pc_next
    # output 30
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_WRITE_IO.value | Signal.SEL_PC_NEXT.value,  # latch_write_io, sel_pc_next
    # input 32
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ACC_IO.value | Signal.SEL_PC_NEXT.value,  # sel_acc_io, sel_pc_next
    # add 34
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_BUFF.value | Signal.SEL_ACC_VAL.value | Signal.SEL_ALU_ADD.value,
    # latch_buff, sel_acc_data_mem, sel_alu_add
    Signal.SEL_PC_NEXT.value,  # sel_pc_next
    # sub 37
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_BUFF.value | Signal.SEL_ACC_VAL.value | Signal.SEL_ALU_SUB.value,
    # latch_buff, sel_acc_data_mem, sel_alu_sub
    Signal.SEL_PC_NEXT.value,  # sel_pc_next
    # mul 40
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_BUFF.value | Signal.SEL_ACC_VAL.value | Signal.SEL_ALU_MUL.value,
    # latch_buff, sel_acc_data_mem, sel_alu_mul
    Signal.SEL_PC_NEXT.value,  # sel_pc_next
    # div 43
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_BUFF.value | Signal.SEL_ACC_VAL.value | Signal.SEL_ALU_DIV.value,
    # latch_buff, sel_acc_data_mem, sel_alu_div
    Signal.SEL_PC_NEXT.value,  # sel_pc_next
    # mod 46
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_BUFF.value | Signal.SEL_ACC_VAL.value | Signal.SEL_ALU_MOD.value,
    # latch_buff, sel_acc_data_mem, sel_alu_mod
    Signal.SEL_PC_NEXT.value,  # sel_pc_next
    # cmp 49
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_CMP_ACC.value | Signal.SEL_PC_NEXT.value,  # sel_cmp_acc, sel_pc_next
    # cntz 51
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_CMP_DC.value | Signal.SEL_PC_NEXT.value,  # sel_cmp_dc, sel_pc_next
    # halt 53
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value | Signal.HLT.value,
]

# Словарь сопоставления Opcode к адресу в массиве микроинструкций
microprogram_addresses = {
    Opcode.LD: 0,
    Opcode.ST: 3,
    Opcode.LDA: 6,
    Opcode.WRITE: 8,
    Opcode.READ: 11,
    Opcode.SETCNT: 14,
    Opcode.SETADDR: 16,
    Opcode.JMP: 18,
    Opcode.JZ: 20,
    Opcode.JGE: 22,
    Opcode.JE: 24,
    Opcode.INC: 26,
    Opcode.DEC: 28,
    Opcode.OUTPUT: 30,
    Opcode.INPUT: 32,
    Opcode.ADD: 34,
    Opcode.SUB: 37,
    Opcode.MUL: 40,
    Opcode.DIV: 43,
    Opcode.MOD: 46,
    Opcode.CMP: 49,
    Opcode.CNTZ: 51,
    Opcode.HLT: 53,
}

microprogram_lengths = {
    Opcode.LD: 3,
    Opcode.ST: 3,
    Opcode.LDA: 2,
    Opcode.WRITE: 3,
    Opcode.READ: 3,
    Opcode.SETCNT: 2,
    Opcode.SETADDR: 2,
    Opcode.JMP: 2,
    Opcode.JZ: 2,
    Opcode.JGE: 2,
    Opcode.JE: 2,
    Opcode.INC: 2,
    Opcode.DEC: 2,
    Opcode.OUTPUT: 2,
    Opcode.INPUT: 2,
    Opcode.ADD: 3,
    Opcode.SUB: 3,
    Opcode.MUL: 3,
    Opcode.DIV: 3,
    Opcode.MOD: 3,
    Opcode.CMP: 2,
    Opcode.CNTZ: 2,
    Opcode.START: 1,
    Opcode.HLT: 1,
}
