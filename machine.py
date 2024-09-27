from __future__ import annotations

import logging
import sys

from isa import WORD_SIZE, Opcode, ProgramData, read_code, read_data
from microcode import Signal, microinstructions, microprogram_addresses, microprogram_lengths


def assert_sel_error(sel: Signal):
    return "internal error, incorrect selector: {}".format(sel)


class DataPath:
    IO_PORTS_BASE_ADDR = 0xFFFC  # Базовый адрес области памяти для портов ввода-вывода
    IO_PORTS_SIZE = 4  # Количество портов
    data_memory: list[int] = None
    data_address: int = None
    buff: int = None
    ports: list[list[int]] = None
    flag_zero: bool
    flag_lt: bool
    flag_gt: bool
    dc: int = None

    def __init__(self, data: list[int], input_data: list[str | int]):
        self.data_memory = data
        self.data_address = 0
        self.acc = 0
        self.buff = 0
        self.ports = [[], [], [], []]
        if input_data:
            self.ports[0] = input_data
        self.flag_zero = False
        self.flag_lt = False
        self.flag_gt = False
        self.dc = 0

    def is_io_address(self, address):
        return self.io_base_addr <= address < self.io_base_addr + self.IO_PORTS_SIZE

    def sel_address_register(self, sel: Signal, addr: int | None = None):
        assert sel in {Signal.SEL_AR_NEXT, Signal.SEL_AR_ADDR, Signal.SEL_AR_ACC}, assert_sel_error(sel)
        if sel == Signal.SEL_AR_NEXT:
            self.data_address += 1
        elif sel == Signal.SEL_AR_ADDR:
            assert addr >= 0, "address register mustn't be negative"
            self.data_address = addr // WORD_SIZE
        elif sel == Signal.SEL_AR_ACC:
            self.data_address = self.acc // WORD_SIZE

    def latch_data_mem(self):
        if self.is_io_address(self.data_address):
            # Запись в порт, отображенный в память
            port_num = self.data_address - self.io_base_addr
            self.ports[port_num].append(chr(self.acc))
        else:
            if self.data_address < len(self.data_memory):
                self.data_memory[self.data_address] = self.acc
            else:
                raise IndexError("OutMEM")

    def latch_buff(self):
        self.buff = self.acc

    def sel_acc(self, sel: Signal, arg: int | None = None):
        assert sel in {Signal.SEL_ACC_IO, Signal.SEL_ACC_VAL, Signal.SEL_ACC_DATA_MEM}, assert_sel_error(sel)
        if sel == Signal.SEL_ACC_IO:
            self.acc = ord(self.ports[arg].pop(0))
        elif sel == Signal.SEL_ACC_VAL:
            self.acc = arg
        elif sel == Signal.SEL_ACC_DATA_MEM:
            if self.is_io_address(self.data_address):
                # Чтение из порта, отображенного в память
                port_num = self.data_address - self.io_base_addr
                if self.ports[port_num]:
                    self.acc = ord(self.ports[port_num].pop(0))
                else:
                    raise IndexError("IO Port is empty")
            else:
                if self.data_address < len(self.data_memory):
                    self.acc = self.data_memory[self.data_address]
                else:
                    raise IndexError("OutMEM")

    def sel_alu(self, sel: Signal):
        assert sel in {
            Signal.SEL_ALU_ADD,
            Signal.SEL_ALU_DEC,
            Signal.SEL_ALU_DIV,
            Signal.SEL_ALU_MOD,
            Signal.SEL_ALU_SUB,
            Signal.SEL_ALU_INC,
            Signal.SEL_ALU_MUL,
        }, assert_sel_error(sel)
        if sel == Signal.SEL_ALU_INC:
            self.acc += 1
        elif sel == Signal.SEL_ALU_DEC:
            self.acc -= 1
        elif sel == Signal.SEL_ALU_SUB:
            self.acc = self.buff - self.acc
        elif sel == Signal.SEL_ALU_ADD:
            self.acc = self.buff + self.acc
        elif sel == Signal.SEL_ALU_MUL:
            self.acc = self.buff * self.acc
        elif sel == Signal.SEL_ALU_DIV:
            self.acc = self.buff // self.acc
        elif sel == Signal.SEL_ALU_MOD:
            self.acc = self.buff % self.acc

    def sel_dc(self, sel: Signal):
        assert sel in {Signal.SEL_DC_ACC, Signal.SEL_DC_DEC}, assert_sel_error(sel)
        if sel == Signal.SEL_DC_ACC:
            self.dc = self.acc
        elif sel == Signal.SEL_DC_DEC:
            self.dc -= 1

    def __compare(self, left: int, right: int):
        self.flag_lt = False
        self.flag_gt = False
        self.flag_zero = False
        if left > right:
            self.flag_gt = True
        elif left < right:
            self.flag_lt = True
        if left == 0:
            self.flag_zero = True

    def sel_cmp(self, sel: Signal, value: int):
        assert sel in {Signal.SEL_CMP_DC, Signal.SEL_CMP_ACC}, assert_sel_error(sel)
        if sel == Signal.SEL_CMP_DC:
            self.__compare(self.dc, value)
        elif sel == Signal.SEL_CMP_ACC:
            self.__compare(self.acc, value)

    def latch_write_io(self, arg: int):
        self.ports[arg].append(chr(self.acc))


class ControlUnit:
    pc: int = None
    program_mem = list[ProgramData]
    mpc: int = None
    mc_program = None
    datapath: DataPath = None
    _tick: int = None

    def __init__(self, program_mem: list[ProgramData], datapath: DataPath):
        self.program_mem = program_mem
        self.datapath = datapath
        self.mpc = 0
        self.mc_program = microprogram_addresses
        self.pc = 0
        self._tick = 0

    def tick(self):
        self._tick += 1

    def current_tick(self):
        return self._tick

    def sel_pc(self, sel_pc: Signal):
        assert sel_pc in {
            Signal.SEL_PC_NEXT,
            Signal.SEL_JMP,
            Signal.SEL_JGE,
            Signal.SEL_JZ,
            Signal.SEL_JE,
        }, assert_sel_error(sel_pc)
        addr: int = self.pc + 1
        if sel_pc == Signal.SEL_PC_NEXT:
            addr = self.pc + 1
        elif sel_pc == Signal.SEL_JMP:
            addr = self.program_mem[self.pc]["args"]
        elif sel_pc == Signal.SEL_JE:
            if not (self.datapath.flag_lt or self.datapath.flag_gt):
                addr = self.program_mem[self.pc]["args"]
        elif sel_pc == Signal.SEL_JGE:
            if self.datapath.flag_gt:
                addr = self.program_mem[self.pc]["args"]
        elif sel_pc == Signal.SEL_JZ:
            if self.datapath.flag_zero:
                addr = self.program_mem[self.pc]["args"]
        self.pc = addr

    def sel_mpc(self, sel: Signal):
        assert sel in {Signal.SEL_MPC_OPC, Signal.SEL_MPC_ZERO, Signal.SEL_MPC_INC}, assert_sel_error(sel)
        if sel == Signal.SEL_MPC_ZERO:
            self.mpc = 0
        elif sel == Signal.SEL_MPC_OPC:
            self.mpc = microprogram_addresses[self.program_mem[self.pc]["cmd"]["opcode"]]
        elif sel == Signal.SEL_MPC_INC:
            self.mpc += 1

    def exec_mp(self):
        arg = self.program_mem[self.pc].get("args", None)
        microinstruction_count = microprogram_lengths[self.program_mem[self.pc]["cmd"]["opcode"]]
        opcode = self.program_mem[self.pc]["cmd"]["opcode"]
        self.sel_mpc(Signal.SEL_MPC_OPC)
        for _ in range(microinstruction_count):
            microinstruction = microinstructions[self.mpc]
            if (microinstruction & Signal.SEL_AR_ADDR.value) == Signal.SEL_AR_ADDR.value:
                self.datapath.sel_address_register(Signal.SEL_AR_ADDR, arg)
            elif (microinstruction & Signal.SEL_AR_ACC.value) == Signal.SEL_AR_ACC.value:
                self.datapath.sel_address_register(Signal.SEL_AR_ACC)
            elif (microinstruction & Signal.SEL_AR_NEXT.value) == Signal.SEL_AR_NEXT.value:
                self.datapath.sel_address_register(Signal.SEL_AR_NEXT)

            if (microinstruction & Signal.LATCH_DATA_MEM.value) == Signal.LATCH_DATA_MEM.value:
                self.datapath.latch_data_mem()

            if (microinstruction & Signal.LATCH_BUFF.value) == Signal.LATCH_BUFF.value:
                self.datapath.latch_buff()

            if (microinstruction & Signal.SEL_ACC_VAL.value) == Signal.SEL_ACC_VAL.value:
                self.datapath.sel_acc(Signal.SEL_ACC_VAL, arg)
            elif (microinstruction & Signal.SEL_ACC_IO.value) == Signal.SEL_ACC_IO.value:
                self.datapath.sel_acc(Signal.SEL_ACC_IO, arg)
            elif (microinstruction & Signal.SEL_ACC_DATA_MEM.value) == Signal.SEL_ACC_DATA_MEM.value:
                self.datapath.sel_acc(Signal.SEL_ACC_DATA_MEM)

            if (microinstruction & Signal.LATCH_WRITE_IO.value) == Signal.LATCH_WRITE_IO.value:
                self.datapath.latch_write_io(self.program_mem[self.pc]["args"])

            if (microinstruction & Signal.SEL_ALU_MOD.value) == Signal.SEL_ALU_MOD.value:
                self.datapath.sel_alu(Signal.SEL_ALU_MOD)
            elif (microinstruction & Signal.SEL_ALU_DIV.value) == Signal.SEL_ALU_DIV.value:
                self.datapath.sel_alu(Signal.SEL_ALU_DIV)
            elif (microinstruction & Signal.SEL_ALU_MUL.value) == Signal.SEL_ALU_MUL.value:
                self.datapath.sel_alu(Signal.SEL_ALU_MUL)
            elif (microinstruction & Signal.SEL_ALU_SUB.value) == Signal.SEL_ALU_SUB.value:
                self.datapath.sel_alu(Signal.SEL_ALU_SUB)
            elif (microinstruction & Signal.SEL_ALU_ADD.value) == Signal.SEL_ALU_ADD.value:
                self.datapath.sel_alu(Signal.SEL_ALU_ADD)
            elif (microinstruction & Signal.SEL_ALU_DEC.value) == Signal.SEL_ALU_DEC.value:
                self.datapath.sel_alu(Signal.SEL_ALU_DEC)
            elif (microinstruction & Signal.SEL_ALU_INC.value) == Signal.SEL_ALU_INC.value:
                self.datapath.sel_alu(Signal.SEL_ALU_INC)

            if (microinstruction & Signal.SEL_DC_ACC.value) == Signal.SEL_DC_ACC.value:
                self.datapath.sel_dc(Signal.SEL_DC_ACC)
            elif (microinstruction & Signal.SEL_DC_DEC.value) == Signal.SEL_DC_DEC.value:
                self.datapath.sel_dc(Signal.SEL_DC_DEC)

            if (microinstruction & Signal.SEL_CMP_DC.value) == Signal.SEL_CMP_DC.value:
                self.datapath.sel_cmp(Signal.SEL_CMP_DC, 0)
            elif (microinstruction & Signal.SEL_CMP_ACC.value) == Signal.SEL_CMP_ACC.value:
                self.datapath.sel_cmp(Signal.SEL_CMP_ACC, arg)

            if (microinstruction & Signal.SEL_JE.value) == Signal.SEL_JE.value:
                self.sel_pc(Signal.SEL_JE)
            elif (microinstruction & Signal.SEL_JGE.value) == Signal.SEL_JGE.value:
                self.sel_pc(Signal.SEL_JGE)
            elif (microinstruction & Signal.SEL_JZ.value) == Signal.SEL_JZ.value:
                self.sel_pc(Signal.SEL_JZ)
            elif (microinstruction & Signal.SEL_JMP.value) == Signal.SEL_JMP.value:
                self.sel_pc(Signal.SEL_JMP)
            elif (microinstruction & Signal.SEL_PC_NEXT.value) == Signal.SEL_PC_NEXT.value:
                self.sel_pc(Signal.SEL_PC_NEXT)

            if (microinstruction & Signal.HLT.value) == Signal.HLT.value:
                self.sel_mpc(Signal.SEL_MPC_ZERO)
                self.tick()
                raise StopIteration

            self.sel_mpc(Signal.SEL_MPC_INC)
            self.tick()


    def __repr__(self):
        instr = self.program_mem[self.pc]
        opcode_name = Opcode(instr["cmd"]["opcode"]).name
        state_repr = (
            f"{opcode_name} {instr.get('args', '')}\n"
            f"TICK: {self._tick:3} "
            f"PC: {self.pc:3} "
            f"ADDR: {self.datapath.data_address:3} "
            f"MEM_OUT: {self.get_mem_out()} "
            f"ACC: {self.datapath.acc} "
            f"BUFF: {self.datapath.buff} "
            f"DC: {self.datapath.dc} "
            f"FLAG_ZERO: {self.datapath.flag_zero} "
            f"FLAG_LT: {int(self.datapath.flag_lt)} "
            f"FLAG_GT: {int(self.datapath.flag_gt)}\n"
            f"INPUT_PORT:  {self.datapath.ports[0]}\n"
            f"OUT_PORT:  {self.datapath.ports[1]}\n"
            f"DATA_MEM:  {self.datapath.data_memory}\n"
            f"---------------------------------------\n"
        )

        return state_repr.strip()  # Удаляем лишние пробелы в конце строки

    def get_mem_out(self):
        try:
            return self.datapath.data_memory[self.datapath.data_address]
        except IndexError:
            return "Out of range"


def simulation(code: list[ProgramData], data: list[int], input_tokens: str | int, limit: int):
    data_path = DataPath(data, input_tokens)
    control_unit = ControlUnit(code, data_path)
    instr_counter = 0

    logging.debug("%s", control_unit)
    try:
        while instr_counter < limit:
            try:
                control_unit.exec_mp()
            except StopIteration:
                break
            instr_counter += 1
            control_unit.tick()
            logging.debug("%s", control_unit)
    except EOFError:
        logging.warning("Input buffer is empty!")

    if instr_counter >= limit:
        logging.warning("Limit exceeded!")

    output_buffer_1 = "".join(data_path.ports[1])
    logging.info("output_buffer: %s", repr(output_buffer_1))
    return output_buffer_1, instr_counter, control_unit.current_tick()


def main(code_file, data_file, input_file):
    code = read_code(code_file)
    data = read_data(data_file)
    with open(input_file, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)

    output, instr_counter, ticks = simulation(code, data, input_token, 300)

    print("".join(output))
    print(f"instr_counter: {instr_counter}, ticks: {ticks}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    assert len(sys.argv) == 4, "Wrong arguments: machine.py <data_file> <code_file> <input_file>"
    _, code_file, data_file, input_file = sys.argv
    main(code_file, data_file, input_file)
