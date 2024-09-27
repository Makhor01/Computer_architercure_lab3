#!/usr/bin/python3
from __future__ import annotations

import re
import sys

from isa import COMMANDS, WORD_SIZE, ProgramData, write_code, write_data

TEXT_ADDR = 0
DATA_ADDR = 0


def get_meaningful_token(line: str):
    return line.split(";", 1)[0].strip()


def translate_stage_1(text: str):
    datasec = text.split("section .data")[1].split("section .text")[0]
    textsec = text.split("section .text")[1]
    data_labels = {}
    code = []
    for data in datasec.splitlines():
        data.strip()
        if data:
            label_name, arg = data.split(":")
            if '"' in arg:
                arg = arg.split('"')[1]
                data_labels[label_name.strip()] = arg
            else:
                data_labels[label_name.strip()] = arg.strip()
    print("Data Labels:", data_labels)  # Отладочный вывод данных
    text_labels = {}
    for line_num, raw_line in enumerate(textsec.splitlines(), 1):
        token = get_meaningful_token(raw_line)
        if token == "":
            continue
        pc = len(code)
        if ":" in token:
            text_labels[token.split(":")[0]] = pc
        else:
            token = token.split()
            arg = ""
            if len(token) == 1:
                cmd = token[0]
                if cmd in COMMANDS:
                    code.append({"addr": pc, "cmd": COMMANDS[cmd]})
                else:
                    print(f"Warning: Command {cmd} not found in COMMANDS at line {line_num}")

            else:
                cmd = token[0]
                arg = token[1]
                if "'" in arg:
                    arg = arg.replace("'", "")
                    arg = arg.replace("\\n", "\n")

                code.append({"addr": pc, "cmd": COMMANDS[cmd], "args": arg})
    print("Text Labels (Stage 1):", text_labels)  # Отладочный вывод меток кода
    print("Code (Stage 1):", code)  # Отладочный вывод инструкций
    return data_labels, text_labels, code


def translate_data_labels_to_addr(data_labels: dict[str]):
    translated_data_labels = {}
    addr_ptr = DATA_ADDR
    for label in data_labels.keys():
        translated_data_labels[label] = {"arg": data_labels[label], "addr": addr_ptr}
        element: str = data_labels[label]
        if re.search(r"res\([0-9]+\)", element):
            addr_ptr += int(element.split("(")[1].split(")")[0]) * WORD_SIZE
        elif not element.isdigit():
            if element in data_labels:
                translated_data_labels[label]["arg"] = str(translated_data_labels[element]["addr"])
            for i in range(len(element)):
                addr_ptr += WORD_SIZE
        else:
            addr_ptr += WORD_SIZE
    print("Translated Data Labels:", translated_data_labels)
    return translated_data_labels


def translate_stage_2(data_labels: dict, text_labels: dict, code: list[ProgramData]):
    translated_data_labels = translate_data_labels_to_addr(data_labels)

    for instruction in code:
        if instruction["cmd"]["args_count"]:
            label = instruction["args"]
            if label.isdigit():
                instruction["args"] = int(label)
            elif label.strip() in data_labels:
                instruction["args"] = translated_data_labels[label]["addr"]
            elif label in text_labels:
                instruction["args"] = text_labels[label]
    print("Final Code (Stage 2):", code)  # Отладочный вывод финального кода
    print("Final Translated Data Labels (Stage 2):", translated_data_labels)  # Отладочный вывод данных
    return code, translated_data_labels


def translate(text):
    data_labels, text_labels, code = translate_stage_1(text)
    code, translated_data_labels = translate_stage_2(data_labels, text_labels, code)
    return code, translated_data_labels


def main(source, program_file, data_file):
    with open(source, encoding="utf-8") as f:
        source = f.read()

    code, translated_data_labels = translate(source)
    # Проверка результатов трансляции перед записью
    if not code:
        print("Warning: No instructions generated!")
    if not translated_data_labels:
        print("Warning: No data labels translated!")
    write_code(program_file, code)
    write_data(data_file, translated_data_labels)
    print("source LoC:", len(source.split("\n")), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 4, "Wrong arguments: translator_asm.py <input_file> <program_file> <data_file> "
    _, input_file, program_file, data_file = sys.argv
    main("examples/hello.asm", "program_file", "data_file")
