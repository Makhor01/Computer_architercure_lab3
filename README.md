# csa_lab3

## Хорошев Максим P3225

## Базовый вариант

```
asm | acc | harv | mc -> hw | tick -> instr | struct | stream | mem | pstr | prob2 | cache
```

## Язык программирование

``` ebnf
<program> ::= <program> <line> | <line>

<line> ::=  <opcode_without_arg>
          | <opcode_transfer> " " <term>
          | <opcode_arg> " (" <term> ")"
          | <opcode_arg> " " <number>
          | <opcode_arg> " " <term>
          | <label>
          | <label> " number " <number>
          | <label> ' string ' '"' <term> '"'
          | "section ." <term>
          | "\n"

<label> ::= <name> ":" (" ")* | <name> ":" (" ")* "\n"

<without_arg> ::= "hlt"
                       | "inc"
                       | "dec"
                       | "read"
                       | "write"
                       | "cntz"
                       | "setcnt"
                       | "setaddr"

<arg> ::= "add" | "mul" | "div" | "mod" | "cmp" | "input" | "output" | "ld" | "lda" | "st"               
<transfer> ::= "jmp" | "jge" | "jz" | "je"
                    
<term> ::= <number> | <letter> | '"' <string> '"'
<letter> ::= [a-z] | [A-Z]
<number> ::= [0-9] <number>*
<string> ::= <letter>*


<name> ::= <letter> (<letter> | <number>)*

```

- `ld`: загружает данные в acc из ячейки памяти (по метке)
- `lda`: загружает в acc указанное значение
- `st`: загружает данные из acc в указанный адрес (по метке)
- `write`: [data_addr] <- [acc], [data_counter] <- [data_counter] - 1, ar <- ar + 1
- `read`:  [data_addr] -> [acc], [data_counter] <- [data_counter] - 1, ar <- ar + 1
- `jmp`: безусловный переход по указанному адресу
- `je` - условный переход по указанному адресу, если после сравнения флаги GT и LT были заполнены нулями
- `jz`: условный переход по указанному адресу, если после сравнения флаг Z был заполнен единицей
- `jge`: условный переход по указанному адресу, если после сравнения флаг GT был заполнен единицей
- `inc`: инкремент аккумулятора. [acc] <- [acc] + 1
- `dec`: декремент аккумулятора. [acc] <- [acc] - 1
- `input`: получение ввода с определенного порта (указывается номер порта)
- `output`: указание порта на вывод (выводится значение из acc)
- `add`: сумма указанного числа с [acc]
- `mul`: умножение указанного числа с [acc]
- `div`: деление значения в acc на указанное число
- `mod`: остаток от деления значения в acc на указанное число
- `hlt`: остановка процессора
- `cntz`: проверка, является ли регистр data_count равен нулю, установка соответствущего флага
- `setcnt`: загрузить значение из аккумулятора в регистр [data_count]
- `сmp`: сравнение значения из аккумулятора с указанным значением
- `setaddr`: устанавливает значение из [acc] в [ar]

## Организация памяти

```
Instruction memory
+------------------------------+
| 00   : program start         |
|     ...                      |
| n    : hlt                   |
+------------------------------+

Data memory
+------------------------------+
| 00   : start_data            |
|     ...                      |
| n    : end_data              |
+------------------------------+
```

- Гарвардская архитектура
- Размер машинного слова
    - Память данных - 32 бит. Один символ - 1 машинное слово.
    - Память команд - 32 бит.
- Адресация
    - Прямая (ld <label>)
    

## Система команд


- Особенности процессора
    - Машинное слово - беззнаковое 32 битное;
    - Доступ к памяти осуществляется через address register;
    

| Номер | Команда | Последовательность сигналов               |
|-------|---------|-------------------------------------------|
| 0     | start   | latch_mpc_zero, latch_mc, sel_pc          |
| 1     | ld      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_ar_addr                               |
|       |         | sel_acc_data_mem, sel_pc_next             |
| 2     | st      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_ar_addr                               |
|       |         | latch_data_mem, sel_pc_next               |
| 3     | lda     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_acc_val, sel_pc_next                  |
| 4     | write   | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_data_mem, sel_dc_dec                |
|       |         | sel_ar_next, sel_pc_next                  |
| 5     | read    | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_acc_data_mem, sel_dc_dec              |
|       |         | sel_ar_next, sel_pc_next                  |
| 6     | setcnt  | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_dc_acc, sel_pc_next                   |
| 7     | setaddr | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_ar_addr, sel_pc_next                  |
| 8     | jmp     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_jmp                                   |
| 9     | jz      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_jz                                    |
| 10    | jge     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_jge                                   |
| 11    | je      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_je                                    |
| 12    | inc     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_alu_inc, sel_pc_next                  |
| 13    | dec     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_alu_dec, sel_pc_next                  |
| 14    | output  | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_write_io, sel_pc_next               |
| 15    | input   | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_acc_io, sel_pc_next                   |
| 16    | add     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_add |
|       |         | sel_pc_next                               |
| 17    | sub     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_sub |
|       |         | sel_pc_next                               |
| 18    | mul     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_mul |
|       |         | sel_pc_next                               |
| 19    | div     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_div |
|       |         | sel_pc_next                               |
| 20    | mod     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_mod |
|       |         | sel_pc_next                               |
| 21    | cmp     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_cmp_acc, sel_pc_next                  |
| 22    | cntz    | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_cmp_dc, sel_pc_next                   |

Описание:

| Номер бита | Сигнал         | Описание                                                                                                            |
|------------|----------------|---------------------------------------------------------------------------------------------------------------------|
| 0          | latch_pm       | Защелкивает значение из памяти по текущему адресу Program Counter.|
| 1          | sel_mpc        | Выбрать микропрограмму по значению Opcode                                                                           |
| 2          |                | 100 - загрузка нуля(при запуске процессора), 110 - загрузка по Opcode                                               |
| 3          |                | 101 - инкремент                                                                                                     |
| 4          | latch_mc       | Защелкивает номер микропрограммы для последующего выполнения. |
| 5          | sel_pc         | 	Определяет следующее значение для Program Counter.                                                                        |
| 6          |                | 1000 - SEL_NEXT, 1001 - SEL_JMP,                                                                                    |
| 7          |                | 1010 - SEL_JZ (в зависимости от флага),                                                                             |
| 8          |                | 1011 - SEL_JE, 1100 - SEL_JGE                                                                                       |
| 9          | sel_ar         | Определяет адрес для обращения к памяти.                                                   |
| 10         |                | 100 - SEL_NEXT, 101 - SEL_ADDR(декодированное значение из CU)                                                       |
| 11         |                | 110 - SEL_AR_ACC                                                                                                    |
| 12         | latch_data_mem | Защелкивает данные из аккумулятора в память по адресу AR.                                                            |
| 13         | sel_acc        | Определяет источник для записи в аккумулятор.                                                                       |
| 14         |                | 100 - SEL_ACC_DATA_MEM, 101 - SEL_ACC_IO(из портов),                                                                |
| 15         |                | 110 - SEL_ACC_VAL(декодированное значение из CU)                                                                    |
| 16         | write_io       | Записывает данные из аккумулятора в порт ввода-вывода.                                                                             |
| 17         | latch_buff     | Защелкивает данные из аккумулятора в буферный регистр.                                                                           |
| 18         | sel_alu        | Определяет операцию для выполнения в АЛУ и записывает результат в аккумулятор..                                                                 |
| 19         |                | 1000 - SEL_ALU_INC, 1001 - SEL_ALU_DEC, 1010 - SEL_ALU_ADD,                                                         |
| 20         |                | 1011 - SEL_ALU_SUB, 1100 - SEL_ALU_MUL, 1101 - SEL_ALU_DIV,                                                         |
| 21         |                | 1110 - SEL_ALU_MOD                                                                                                  |
| 22         | sel_dc         | Определяет значение для регистра Data Count.                                                                  |
| 23         |                | 10 - SEL_DC_DEC(декремент) 11 - SEL_DC_ACC (из аккумулятора)                                                        |
| 24         | sel_cmp        | Выбор левого входа для сравнения с декодированным значением из CU.                                                  |
| 25         |                | 10 - SEL_CMP_ACC(значение из аккумулятора), 11 - SEL_CMP_DC(значение из data counter)                               |

## Транслятор

Интерфейс командной строки: `python3 translator.py <source_input_file> <program_file> <data_file>`


Трансляция секции .data:

- translate_stage1:
    - Разделяет данные на токены, возвращает данные
      в формате <label>:<addr>, а код в формате {<addr>, <command>, <args>}.
      Также на этой стадии вернуться текстовые метки,
      которым будет соответствовать значение pc на котором они встретились.

- translate_data_labels_to_addr:
    - Вычисляет адреса для меток в памяти, выделяет необходимое адресное пространство для res(<number>)
- translate_stage2:
    - Вставляет адреса меток данных и команд в аргументы инструкций.

Правила:

- .data и .text должны присутствовать в программе, даже если они пустые
- Одна строка - одна инструкция

## Модель процессора

DataPath

![DataPath.png](schemes%2FDataPath.png)
ALU (Арифметико-логическое устройство): Выполняет арифметические и логические операции, такие как сложение, вычитание, умножение и деление.

I/O Devices: Здесь происходит взаимодействие с устройствами ввода-вывода. В вашей программе это может быть реализовано через специальные порты ввода-вывода, отображённые в память.

Accumulator (ACC): Регистр-накопитель, который хранит промежуточные результаты вычислений.

Data Memory: Память данных, которая используется для хранения переменных и других данных программы.

Buffer Register (BUFF): Используется для временного хранения данных при выполнении операций с памятью и устройствами.
## Control Unit



![ControlUnit.png](schemes%2FControlUnit.png)
Program Counter (PC): Хранит адрес текущей команды в памяти программы. После выполнения команды PC инкрементируется или изменяется в зависимости от условий переходов (например, JUMP или условные переходы).

Program Memory: Хранит последовательность команд программы, которая выполняется. В каждой команде указана операция и её аргументы.

Opcode -> currentMC: Этот компонент преобразует текущий код операции (opcode) в адрес соответствующего микрокода. Он управляет выбором нужной микропрограммы для выполнения команды.

Next MC и MUX: Эти компоненты выбирают следующую микрокоманду для выполнения, основываясь на текущем состоянии и управляющих сигналах. Они помогают переходить от одной микрокоманды к другой.

MC Program (Микропрограмма): Это память, в которой хранится микрокод для управления DataPath и другими компонентами системы. Выполняется цикл выполнения команд с помощью микрокодов.

## Тестирование

Golden - тестирование.

Директория с тестами: `./golden`

Директория с генерацией логов тестов для отдельного просмотра-изменения `./logs`

Исполняемый файл: `golden_test.py`

## CI

```
name: CI Pipeline

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run tests and collect coverage
        run: |
          poetry run coverage run -m pytest .
          poetry run coverage report -m
        env:
          CI: true

      lint:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Check code formatting with Ruff
        run: poetry run ruff format --check .

      - name: Run Ruff linters
        run: poetry run ruff check .
name: Python CI

```

## Отчёт на примере hello.asm

Исходный код:

```nasm
section .data
message_size: 13
message: "Hello, world!"
section .text
_start:
    ld message_size
    setcnt
    lda message
    setaddr
    loop:
        read
        output 1
        cntz
        jz exit
        jmp loop
    exit:
        hlt
```

Отформатированные данные

```python
  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
```

Журнал:

```
DEBUG   machine:simulation    LD 0
    TICK:   0 PC:   0 ADDR:   0 MEM_OUT: 13 ACC: 0 BUFF: 0 DC: 0 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    SETCNT 
    TICK:   4 PC:   1 ADDR:   0 MEM_OUT: 13 ACC: 13 BUFF: 0 DC: 0 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    LDA 4
    TICK:   7 PC:   2 ADDR:   0 MEM_OUT: 13 ACC: 13 BUFF: 0 DC: 13 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    SETADDR 
    TICK:  10 PC:   3 ADDR:   0 MEM_OUT: 13 ACC: 4 BUFF: 0 DC: 13 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  13 PC:   4 ADDR:   1 MEM_OUT: 72 ACC: 4 BUFF: 0 DC: 13 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  17 PC:   5 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  20 PC:   6 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  23 PC:   7 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  26 PC:   8 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  29 PC:   4 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  33 PC:   5 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  36 PC:   6 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  39 PC:   7 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  42 PC:   8 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  45 PC:   4 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  49 PC:   5 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  52 PC:   6 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  55 PC:   7 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  58 PC:   8 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  61 PC:   4 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  65 PC:   5 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  68 PC:   6 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  71 PC:   7 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  74 PC:   8 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  77 PC:   4 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  81 PC:   5 ADDR:   6 MEM_OUT: 44 ACC: 111 BUFF: 0 DC: 8 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  84 PC:   6 ADDR:   6 MEM_OUT: 44 ACC: 111 BUFF: 0 DC: 8 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l', 'o']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
  ......
  
  ---------------------------------------
    INFO    machine:simulation    output_buffer: 'Hello, world!'
```
