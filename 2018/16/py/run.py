#! /usr/bin/python3

import sys
import os
import time
import re
from typing import Dict, List, Set, Tuple

Registers = Tuple[int, int, int, int]
Operation = Tuple[int, int, int, int]
Record = Tuple[Registers, Operation, Registers]
MNEMONICS = [
    "addr", "addi",
    "mulr", "muli",
    "banr", "bani",
    "borr", "bori",
    "setr", "seti",
    "gtir", "gtri", "gtrr",
    "eqir", "eqri", "eqrr"
]


def run_operation(registers: Registers, operation: Operation, mnemonic: str) -> Registers:
    _, a, b, c = operation
    result = list(registers)
    value = -1
    if mnemonic == "addr":
        value = registers[a] + registers[b]
    elif mnemonic == "addi":
        value = registers[a] + b
    elif mnemonic == "mulr":
        value = registers[a] * registers[b]
    elif mnemonic == "muli":
        value = registers[a] * b
    elif mnemonic == "banr":
        value = registers[a] & registers[b]
    elif mnemonic == "bani":
        value = registers[a] & b
    elif mnemonic == "borr":
        value = registers[a] | registers[b]
    elif mnemonic == "bori":
        value = registers[a] | b
    elif mnemonic == "setr":
        value = registers[a]
    elif mnemonic == "seti":
        value = a
    elif mnemonic == "gtir":
        value = 1 if a > registers[b] else 0
    elif mnemonic == "gtri":
        value = 1 if registers[a] > b else 0
    elif mnemonic == "gtrr":
        value = 1 if registers[a] > registers[b] else 0
    elif mnemonic == "eqir":
        value = 1 if a == registers[b] else 0
    elif mnemonic == "eqri":
        value = 1 if registers[a] == b else 0
    elif mnemonic == "eqrr":
        value = 1 if registers[a] == registers[b] else 0
    result[c] = value
    return tuple(result)


def test_record(before: Registers, operation: Operation, after: Registers, opcodes: Dict[str, Set[int]]) -> int:
    count = 0
    opcode, *_ = operation
    for mnenomic in MNEMONICS:
        if after == run_operation(before, operation, mnenomic):
            if -opcode not in opcodes[mnenomic]:
                opcodes[mnenomic].add(opcode)
            count += 1
        elif opcode in opcodes[mnenomic]:
            opcodes[mnenomic].remove(opcode)
            opcodes[mnenomic].add(-opcode)
    return count


def solve(puzzle_input: Tuple[List[Record], List[Operation]]) -> Tuple[int, int]:
    records, program = puzzle_input
    opcodes: Dict[str, Set[int]] = {mnemonic: set() for mnemonic in MNEMONICS}
    three_or_more = 0
    for before, operation, after in records:
        if test_record(before, operation, after, opcodes) >= 3:
            three_or_more += 1
    for mnemonic, valid in opcodes.items():
        opcodes[mnemonic] = {op for op in valid if op >= 0}
    while any(len(valid) > 1 for valid in opcodes.values()):
        single_valid = [next(iter(valid))
                        for valid in opcodes.values() if len(valid) == 1]
        for _, valid in opcodes.items():
            if len(valid) > 1:
                for single in single_valid:
                    if single in valid:
                        valid.remove(single)
    ops = {next(iter(valid)): mnemonic for mnemonic, valid in opcodes.items()}
    registers = (0, 0, 0, 0)
    for op in program:
        registers = run_operation(registers, op, ops[op[0]])
    return three_or_more, registers[0]


record_regex = re.compile(
    r"Before: \[(?P<b0>\d+), (?P<b1>\d+), (?P<b2>\d+), (?P<b3>\d+)]\n(?P<opCode>\d+) (?P<A>\d) (?P<B>\d) (?P<C>\d)\nAfter:  \[(?P<a0>\d+), (?P<a1>\d+), (?P<a2>\d+), (?P<a3>\d+)]")
operation_regex = re.compile(r"(?P<opCode>\d+) (?P<A>\d) (?P<B>\d) (?P<C>\d)")


def get_input(file_path: str) -> Tuple[List[Record], List[Operation]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        records_text, program_text = file.read().split("\n\n\n\n")
        records: List[Record] = []
        for match in record_regex.finditer(records_text):
            records.append((
                (int(match.group("b0")), int(match.group("b1")),
                 int(match.group("b2")), int(match.group("b3"))),
                (int(match.group("opCode")), int(match.group("A")),
                 int(match.group("B")), int(match.group("C"))),
                (int(match.group("a0")), int(match.group("a1")),
                 int(match.group("a2")), int(match.group("a3")))
            ))
        operations: List[Operation] = []
        for match in operation_regex.finditer(program_text):
            operations.append((int(match.group("opCode")), int(
                match.group("A")), int(match.group("B")), int(match.group("C"))))
        return records, operations


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
