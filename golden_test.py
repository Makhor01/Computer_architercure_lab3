import binascii
import contextlib
import io
import logging
import os
import tempfile

import machine
import pytest
import translator


def binary_to_hex(binary_data):
    return binascii.hexlify(binary_data).decode("utf-8")


def hex_to_binary(hex_data):
    return binascii.unhexlify(hex_data.encode("utf-8"))


@pytest.mark.golden_test("golden/*_asm.yml")
def test_translator_asm_and_machine(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.asm")
        input_stream = os.path.join(tmpdirname, "input_file")

        target_code = os.path.join(tmpdirname, "program_file")
        target_data = os.path.join(tmpdirname, "data_file")
        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["in_source"])
        with open(input_stream, "w", encoding="utf-8") as file:
            if golden["in_stdin"]:
                file.write(golden["in_stdin"] + "\n")
            else:
                file.write("")

        log_file_path = os.path.join(f"./logs/log_output_{golden.path.name}")

        logger = logging.getLogger()
        file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)-7s %(module)s:%(funcName)-13s %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                translator.main(source, target_code, target_data)
                print("============================================================")
                machine.main(target_code, target_data, input_stream)
        finally:
            logger.removeHandler(file_handler)
            file_handler.close()

        with open(target_code, "rb") as file:
            code = file.read()

        with open(target_data, "rb") as file:
            data = file.read()

        assert binary_to_hex(code).strip() == golden.out["out_code"].strip()
        assert binary_to_hex(data).strip() == golden.out["out_data"].strip()
        assert stdout.getvalue().strip() == golden.out["out_stdout"].strip()
        assert caplog.text.strip() == golden.out["out_log"].strip()
